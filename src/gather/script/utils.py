# -*- coding: utf-8 -*-
'''
Created on 2015年1月12日

@author: heyuxing
'''
import urllib2, cookielib, urllib

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

'''
URL特殊字符转义
'''            
def urlzhuanyi(in_url):
    in_url = in_url.replace("&amp;","&")    
    return in_url
    
'''
获得inUrl请求数据的结果htmlsrc
inUrl：请求链接
post_datas：post数据
inUrl前缀做判断：如果是文件则读取文件内容返回，如果是文本内容则直接返回该内容，如果是url则返回该url应答页面的内容。
'''
def getUrlContent(inUrl,post_datas={}):
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
           
    if inUrl.startswith("file:///"):
        tmp_file = open(inUrl[8:],"r")
        filesrc = tmp_file.read()
        tmp_file.close()
        print "request: "+str(inUrl)
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
#         headers = {
#             "Host": "weixin.sogou.com",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
#             "Accept-Encoding": "gzip, deflate",
#             "Cookie": "CXID=7B2FDDA4C4F052374394085AAD8B98A3; SUID=1EC5E7655709950A538835A0000DEB93; SUV=001B04B565E7C51E538D3B37E8AD5410; IPLOC=CN3100; ssuid=7548319840; pgv_pvi=4598510592; ABTEST=7|1421028691|v1; SNUID=CD1134B6D3D6DFB9485FEDC0D4C04012; sct=1; LSTMV=9%2C17; LCLKINT=1029035",
#             "Connection": "keep-alive",
#         }
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
                if post_datas:
                    url_data = urllib.urlencode(post_datas)
                    resp = urllib2.urlopen(req, url_data)   #inUrl
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
            print err
            return None
    return htmlsrc


if __name__ == "__main__":   
    print getUrlContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page=1")
    
    
    
