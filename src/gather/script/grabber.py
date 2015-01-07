# -*- coding: utf-8 -*-

from Queue import Queue
import re
import threading
import urllib2, cookielib

import stdb


default_jobsetting = {"html_encoding":"GBK","parse_encoding":"utf-8"}
jobpath = []
outfile = None
urlCheckedList = {}
output_path = "test.txt"

wdg = {}


class HTTPRefererProcessor(urllib2.BaseHandler):
    def __init__(self):
        self.referer = None
    
    def http_request(self, request):
        if ((self.referer is not None) and
            not request.has_header("Referer")):
            request.add_unredirected_header("Referer", self.referer)
        return request

    def http_response(self, request, response):
        self.referer = response.geturl()
        return response
        
    https_request = http_request
    https_response = http_response

    

class ErrorHandler(urllib2.HTTPDefaultErrorHandler):  
    def http_error_default(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)  
        result.status = code  
        return result
    
def urlzhuanyi(in_url):
    in_url = in_url.replace("&amp;","&")    
    return in_url

def masktoblank(instr):

    instr = instr.replace(chr(13),"")
    instr = instr.replace(chr(10),"")
    instr = instr.replace(chr(9),"")
    instr = instr.replace("&nbsp;","")

    #去掉标签
    normalTagreg =re.compile("(<\s*(?:span|a|font|p|h|h1|h2|h3|)?[^>]*>)")
    tags = normalTagreg.findall(instr)
    for tagstr in tags:
        instr = instr.replace(tagstr,"")
        
    return instr

#inUrl前缀做判断：如果是文件则读取文件内容返回，如果是文本内容则直接返回该内容，如果是url则返回该url应答页面的内容
def getUrlContent(inUrl,postdata=None):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cj),
            HTTPRefererProcessor(),
        )
    urllib2.install_opener(opener)
        
    if len(inUrl)==0:
        #print "get blank url"
        return ""
    inUrl = urlzhuanyi(inUrl)
    #print "call getUrlContent"
           
    if inUrl.startswith("file:///"):
        tmp_file = open(inUrl[8:],"r")
        filesrc = tmp_file.read()
        tmp_file.close()
        print "request: "+str(inUrl)
        #print "done getUrlContent"
        return filesrc
    elif inUrl.startswith("inline:///"):
        return inUrl[10:]
       
    tpnum = 5    #url请求出错时重试多次（5次）
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-cn,zh;q=0.5",
        "Accept-Charset":"gb2312,utf-8;q=0.7,*;q=0.7",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "Cookie":"skin=noskin; path=/; domain=.amazon.com; expires=Wed, 25-Mar-2009 08:38:55 GMT\r\nsession-id-time=1238569200l; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT\r\nsession-id=175-6181358-2561013; path=/; domain=.amazon.com; expires=Wed Apr 01 07:00:00 2009 GMT"
    }

    req=urllib2.Request(inUrl,headers=headers) #伪造request的header头，有些网站不支持，会拒绝请求;有些网站必须伪造header头才能访问
    htmlsrc = ""
    while len(htmlsrc)==0 and tpnum>0:
        try:
            print "request: "+str(inUrl)
            #page = mgr.open(req)
            import socket
            s=socket.socket()
            socket.setdefaulttimeout(25)
            s.setblocking(0)
            try:
                resp = None
                if postdata is not None:
                    #url_data = urllib.urlencode(postdata)
                    resp = urllib2.urlopen(req)   #inUrl
                else:
                    print inUrl
                    resp = urllib2.urlopen(req)

                htmlsrc =resp.read()                
                tpnum = 0
            except:
                print "request time out",tpnum
                htmlsrc = ""
                tpnum = tpnum - 1
        except urllib2.URLError,err:
            print "error getUrlContent"
            print err
            return None
    return htmlsrc

#移除html标签，特别的：br标签替换成一个空格
def removetag(src,inTag):
    
    chunk_list = []
    tag_head = "<"+inTag
    b_pos = src.find(tag_head)
    e_pos = 0
    while b_pos>=0 and e_pos>=0:
        if inTag.startswith("br"):
            chunk_list.append(src[e_pos:b_pos]+" ")
        else:
            chunk_list.append(src[e_pos:b_pos])
        e_pos = src.find(">",b_pos)+1
        b_pos = src.find(tag_head,e_pos)
    if b_pos == -1 and e_pos >=0:
        chunk_list.append(src[e_pos:])
    return ''.join(chunk_list)

#raw_url:获取页面的链接
#parse_stepset:解析页面的规则
#运行时的一些状态，中间值、解析结果等
def regpagedata(raw_url,parse_stepset,runtime_status,postdata=None):
                                    
    global default_jobsetting, wdg
    
    #获取raw_url的应答页面，并处理好编码问题
    param_retrieve_str = re.compile(r'\$\{([^}]*)\}')
    params = param_retrieve_str.findall(raw_url)    
    for items in params:
        if items not in runtime_status:
            print "can't find "+items+" in runtime status when reg page data. "
            return []
        raw_url = raw_url.replace('${'+items+'}',runtime_status[items])
    #print str(runtime_status)
   
    page_encoding = default_jobsetting["html_encoding"]
    if "encoding" in parse_stepset:
        page_encoding = parse_stepset["encoding"]
    raw_url = raw_url.decode("UTF-8","ignore").encode(page_encoding,"ignore")
    page_src = getUrlContent(raw_url,postdata)
    #if raw_url not in wdg:
    #    tmp_file = open("111"+str(len(raw_url))+".html","w")
    #    tmp_file.write(raw_url)
    #    tmp_file.write("\n\n")
    #    tmp_file.write(page_src)
    #    tmp_file.write("\n\n")        
    #    tmp_file.close()
    #    wdg[raw_url] = 1
   
    if page_encoding == "unicode":
        page_src = eval("u'"+page_src+"'").encode(default_jobsetting["parse_encoding"],"ignore")
    else:
        page_src = page_src.decode(page_encoding,"ignore").encode(default_jobsetting["parse_encoding"],"ignore")

    
    #开始解析获得页面page_src      

    #依据块的定位符，从应答页面中分理出需要详细解析的结果块，可以有多块结果
    rtv = [{}]
    if "block_matchs" in parse_stepset:
        rtv = []
        print parse_stepset
        bstr = parse_stepset["block_matchs"]["start_str"]
        estr = parse_stepset["block_matchs"]["end_str"]
        prex = parse_stepset["block_matchs"]["result"]
        tmp_src = page_src.replace("\n","").replace("\r","")
        
        b_pos = tmp_src.find(bstr)
        block_num = 0
        #if b_pos<0:
        #    print "can't find "+bstr+" in "+page_src
        while b_pos >= 0:
            block_num += 1
            e_pos = tmp_src.find(estr,b_pos+len(bstr))
            rtv.append({prex:tmp_src[b_pos:e_pos]})
            if e_pos>=0:
                b_pos = tmp_src.find(bstr,e_pos)
            else: #未找到结束块e_pos为负值，跳出while循环
                b_pos = e_pos
        print  prex,block_num
        if len(rtv) == 0:
            rtv =[{}]
            
    #--------------------------------------------TODO
    #解析结果页面，需要再分析。   
    parse_regular_matchs = parse_stepset["regular_matchs"]  
    for regular_matchs in parse_regular_matchs:
        is_unique = regular_matchs["is_unique"]
        datalist = []
        #使用exp中的正则表达式匹配出相关结果
        for data_ret_str in regular_matchs["regular"]:
            tmp_src = page_src
            if 'omittag' in regular_matchs:
                for omittag in regular_matchs['omittag']:
                    tmp_src = removetag(tmp_src,omittag)
            pagedata_ret = re.compile(data_ret_str)
            tmp_datalist = pagedata_ret.findall(tmp_src)
            if len(tmp_datalist)>0:
                for items in tmp_datalist:
                    datalist.append(items)
            
        #正则表达式未匹配到值时，前面的解析结果中有相关值则赋值到datalist中   
        if len(datalist)==0:
            tmp_list = []
            tmp_n = 0
            while (regular_matchs["result"]+str(tmp_n)) in runtime_status:
                tmp_list.append("n/a")
                tmp_n = tmp_n + 1
            if len(tmp_list)>0:
                datalist.append(tmp_list) 
            
        tmp_addon_list = []           
               
        scroll_str = ""                    
        for data_i in range(0,len(datalist)):
            #如果is_unique等于一，则只取匹配结果中的第一个值。等于0时取所有的结果
            if is_unique == "1" and data_i>0:
                continue          
            data = datalist[data_i]
            grub_status = {}

            if type(data) == type("a"):
                grub_status[regular_matchs["result"]+"1"]=data
                scroll_str = scroll_str + data + "||"
            else:
                for i in range(0,len(data)):                    
                    grub_status[regular_matchs["result"]+str(i+1)]=data[i]
                    scroll_str = scroll_str + data[i] + "||"            

            if "is_scroll" not in regular_matchs or regular_matchs["is_scroll"]!="1":
                for items in rtv:
                    tmp_map = {}
                
                    for tmp_iks1 in grub_status.keys():
                        tmp_map[tmp_iks1] = grub_status[tmp_iks1]
                        
                    for tmp_iks1 in items.keys():
                        tmp_map[tmp_iks1] = items[tmp_iks1]                        
                             
                    tmp_addon_list.append(tmp_map)      
        if "is_scroll" not in regular_matchs or regular_matchs["is_scroll"]!="1":
            if len(tmp_addon_list) == 0:
                tmp_addon_list = [{}]
            #print str(tmp_addon_list)
            else:
                rtv = []
                for items in tmp_addon_list:
                    if len(items)>0:
                        rtv.append(items)
        else:
            tmp_addon_list = []
            for items in rtv:
                if len(items)>0:
                    tmp_addon_list.append(items)
                
            rtv = []
            if len(tmp_addon_list)==0:
                tmp_addon_list = [{}]
            for items in tmp_addon_list:
                items[regular_matchs["result"]] = scroll_str
                rtv.append(items)

    return rtv

#占位符替换为实际值：in_url中包含占位符${}，runtime_status中存储了占位符的实际值
def urlinsocket(in_url,runtime_status):
    
    param_retrieve_str = re.compile(r'\$\{([^}]*)\}')
    params = param_retrieve_str.findall(in_url)
    for items in params:
        if items not in runtime_status:
            print "can't find "+items+" in runtime status when urlinsocket"
            return ""
        in_url = in_url.replace('${'+items+'}',str(runtime_status[items]))
    return in_url
    


    
class GatherWorker(threading.Thread):
    
    def __init__(self, threadname, jobpath, queue,output_queue):
        
        threading.Thread.__init__(self, name = threadname)
        #执行抓取的线程队列
        self.sharedata = queue
        #抓取规则
        self.jobpath = jobpath
        #输出队列
        self.output_queue = output_queue


    def run(self):

        print self.getName(),'Started'
        
        while True:            
            items = self.sharedata.get()
            self.parsePage(items[0],items[1])
            self.sharedata.task_done()           
        
        print self.getName(),'Finished'

    #根据输出列表output_keys的规则将抓取结果runtime_status（一条结果，即一行结果）整理后存入output_queue
    def outputvalues(self,output_keys,runtime_status):
    
        output_v = []
        for kys in output_keys:
            if kys in runtime_status:
                output_v.append(masktoblank(runtime_status[kys]))
                #print masktoblank(runtime_status[kys])
            elif kys.endswith("*"):
                prex_key = kys[:-1]
                n = 1
                while prex_key+str(n) in runtime_status:
                    output_v.append(masktoblank(runtime_status[prex_key+str(n)]))                   
                    n = n+1
            elif kys.startswith("$"):
                output_v.append(kys[1:])
            else:
                output_v.append("n\\a")

        #self.dbpt.writeData([output_v,])
        self.output_queue.put(output_v)        

    #根据所写的正则表达式执行抓取，并将结果存入output_queue
    def parsePage(self,parse_step,runtime_status):
    
        print "parsePage call" + str(parse_step)
        next_status = {}
        if parse_step>= len(self.jobpath):
            return
        #所有的抓取规则都执行了，到了输出列表处，根据规则将结果存入output_queue
        if parse_step == len(self.jobpath)-1:
        #and jobpath[parse_step]["is_end"] == "1":
            self.outputvalues(self.jobpath[parse_step]["output_keys"],runtime_status)
            
        if "reCheck" in self.jobpath[parse_step] and self.jobpath[parse_step]["reCheck"]=="1":
            runtime_status["reCheck"] = 1
        else:
            runtime_status["reCheck"] = 0
        status_list = []
        #所有的抓取规则都执行了，到了输出列表处（字典self.jobpath[parse_step]不包含url这个key），结束抓取
        if "url" not in self.jobpath[parse_step]:
            return
        #执行parse_step该步的抓取：parse_step在这个循环处没有自增，遍历的是url的集合
        for p_u in self.jobpath[parse_step]["url"]:
            if parse_step == 0:
                tmp_pathlist = p_u.split("/")
                runtime_status["page_path"] = p_u[:p_u.find(tmp_pathlist[-1])]

            raw_url = urlinsocket(p_u,runtime_status)
            if raw_url == None or raw_url == "":
                if "callprint" in self.jobpath[parse_step] and self.jobpath[parse_step]["callprint"]=="1":
                    print "halt then call print "
                    self.sharedata.put((len(self.jobpath)-1,runtime_status))
                return
            
            if "postdata" in self.jobpath[parse_step]:
                status_list = regpagedata(raw_url,self.jobpath[parse_step],runtime_status,self.jobpath[parse_step]["postdata"])
            else:
                status_list = regpagedata(raw_url,self.jobpath[parse_step],runtime_status,None)

            print "return list : "+str(len(status_list))
            
            if len(status_list) ==0 or ( len(status_list) == 1 and len(status_list[0]) == 0 ):
                if "callprint" in self.jobpath[parse_step] and self.jobpath[parse_step]["callprint"]=="1":
                    print "halt then call print "
                    self.sharedata.put((len(self.jobpath)-1,runtime_status))
                return
            
            
            #解析结果status_list和解析时的中间结果runtime_status合并，并将合并的结果用于下一步的解析
            for tmp_status in status_list:
                if len(tmp_status)==0:
                    continue
                #outfile.write(str(tmp_status)+"\n")
                if type(tmp_status) == type({}):
                    next_status = {}
                    for rts_ks in runtime_status:
                        next_status[rts_ks] = runtime_status[rts_ks]
                    for tmp_ks in tmp_status:
                        next_status[tmp_ks] = tmp_status[tmp_ks]               
              
                    #parsePage(parse_step+1,self.jobpath,next_status)
                    self.sharedata.put((parse_step+1 ,next_status))
                else:
                    print "status error "+str(tmp_status)
            #start page loop
        #is_need_loop等于一时处理循环抓取的情况，可以按照loop_url抓取下一页，还可以设置分页步进长度，分页数目
        hasNext = True
        lastUrl = ""
        for raw_loop_url in self.jobpath[parse_step]["loop_url"]:
            hasNext = True
            lastUrl = ""
            while self.jobpath[parse_step]["is_need_loop"] == "1" and hasNext:            
                status_list = [{}]
                if "loopset" in self.jobpath[parse_step]:                        
                    loopset = self.jobpath[parse_step]["loopset"]
                    offset_str = loopset["offset"]
                    limit = loopset.get('limit', 0)
                    
                    print loopset,limit
                    limit = int(limit)
                    if offset_str not in next_status:
                        next_status[offset_str] = '1'
                    next_status[offset_str] = str(int(loopset["step"]) + int(next_status[offset_str]))
                    offset = next_status[offset_str]
                    runtime_status[offset_str] = offset
                    print int(next_status[offset_str]), limit
                    if limit<=0:
                        pass
                    elif int(next_status[offset_str]) > limit:
                        print int(next_status[offset_str]), limit
                        print int(next_status[offset_str]) > limit
                        hasNext = False
                        break
                   
                next_url = urlinsocket(raw_loop_url,next_status)                
                
                if len(next_url) == 0 or next_url == lastUrl:            
                    hasNext = False
                else:
                    lastUrl = next_url            
                    
                    status_list = regpagedata(raw_loop_url,self.jobpath[parse_step],next_status)                    
                    
                    for status in status_list:                
                        if type(status) == type({}):
                            next_status = {}                            
                            for rts_ks in runtime_status:
                                next_status[rts_ks] = runtime_status[rts_ks]
                            for tmp_ks in status:
                                next_status[tmp_ks] = status[tmp_ks]               
                
                            #parsePage(parse_step+1,self.jobpath,next_status)
                            #抓取队列下一步
                            self.sharedata.put((parse_step+1 ,next_status))
        return

#将结果output_queue输出的最终的txt文件中
class OutputFileScanResult(threading.Thread):
    from microscope.settings import BASE_DIR
    outputfilename = BASE_DIR+"/gather/script/OutputFileScanResult.txt"
    
    def __init__(self, threadname, scan_id, output_queue):
        
        threading.Thread.__init__(self, name = threadname)
        self.scan_id = scan_id
        self.sharedata = output_queue

    def run(self):

        print self.name,'Started'        
            
        while True:
            items = self.sharedata.get()
            self.outputfile = open(self.outputfilename,"a")
            for item in items:
                self.outputfile.write(item)
                self.outputfile.write("\t")
            self.outputfile.write("\n")
            self.outputfile.close()
            self.sharedata.task_done()
        
#抓取的主程序：在数据库中设置抓取前的任务状态，启动抓取线程，启动输出抓取结果的线程，在数据库中设置抓取任务的状态
class Grabber(object):

    def __init__(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        #抓取规则
        self.jobpath = []
        self.urlCheckedList = {}        
        self.dbpt = stdb.dbpipe()
        self.grbQueue = Queue()  #抓取队列      
        self.output_queue = Queue()    #结果输出队列
        self.cgqueue = Queue()
        
    def startscan(self, job_id, job_name="", get_rules="",placeholders={}, thread_num=1):
        #TODO
        from gather.rule.models import PageInfo
        pageInfo = PageInfo()
        pageInfo.url = "www.baidu.com"
        print pageInfo.url
        #
        self.dbpt.prepareScan(job_id, job_name=job_name, get_rules=get_rules, placeholders=placeholders, thread_num=thread_num)
        #
        self.jobpath = self.dbpt.jobsetting
        
        runtime_status = {}
        #启动抓取线程，线程处于ready状态
        for i in range(thread_num):
            t = GatherWorker("GatherWorker_"+str(i), self.jobpath,self.grbQueue, self.output_queue)
            t.setDaemon(True)
            t.start()
        #创建输出最终结果的txt，启动输出结果的线程，线程处于ready状态
        #清空输出结果文件
        outputfile = open(OutputFileScanResult.outputfilename,"w")
        outputfile.close()
        #将结果输出到文件
        for i in range(0,1):
            t = OutputFileScanResult(threadname="OutputFileScanResult_"+str(i), scan_id=self.dbpt.scan_id, output_queue=self.output_queue)
            t.setDaemon(True)
            t.start()            
        
        #设置抓取第一步，用第一个正则语句块进行抓取。（广度优先）
        self.grbQueue.put((0,runtime_status))
        #等待grbQueue线程队列结束
        self.grbQueue.join()
        #等待output_queue队列结束
        self.output_queue.join()   
        
        #将结果文件内容输出到数据库
        outputfile = open(OutputFileScanResult.outputfilename,"r")
        line = outputfile.readline()    # 调用文件的 readline()方法
        while line:
            from gather.job.models import ScanResult
            scanResult = ScanResult(scan_id=self.dbpt.scan_id, scan_result=line.strip('\n'))
            scanResult.save()
            print line.strip('\n')
            line = outputfile.readline()
        outputfile.close()
        
        #
        self.dbpt.finishscan()
        print "finish"
        
        return
    
    

if __name__ == "__main__":   
#     print "just import it"
#     getUrlContent('http://sr.ju690.cn?orderby=new&dismode=discuss&day=7&p=page2')
    src = '<div class="star clearfix"><span class="allstar45"></span><span class="rating_nums">8.4</span><span class="pl">(293人评价)</span></div>'
    print src
    src = removetag(src,"span")
    print src
    src = removetag(src,"/span")
    print src
    src = removetag(src,"div")
    print src

    
    


