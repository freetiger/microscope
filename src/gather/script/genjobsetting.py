# -*- coding: utf-8 -*-
import pickle
#start
jobpath = []

jobpath.append({
        "urls":['http://songshuhui.net/archives/tag/%E5%8E%9F%E5%88%9B',],
        "regular_matchs":[{        
        "result":"nextPageUrl",
        "regulars":['<a class="nextpostslink" href="([^"]*)"[^>]*>[^<]*</a>',],
        "is_unique":"1",
        }, ],
       "block_match":{"start_str":'<html>',"end_str":'</html>',"result":"comblock"},
       "encoding":"UTF-8",
       "is_need_loop":"1",
       "loopset":{"offset":"{{offset}}", "limit":"{{limit}}", "step":"{{step}}", },
       "loop_url":["${nextPageUrl1}",],
       "job_description":"科学松鼠会-原创列表"
    })

jobpath.append({
    "urls":['inline:///${comblock}',],
    "regular_matchs":[{        
        "result":"title",
        "regulars":['<h3 class="storytitle"><a class="black" href="([^"]*)"[^>]*>([^<]*)</a></h3>',],
        "is_unique":"0",
        },],
   "encoding":"UTF-8",
   "is_need_loop":"0",
   "loop_url":[],
   "job_description":"科学松鼠会-原创标题链接"
})

jobpath.append({"is_end":"1","output_keys":["title1","title2",]})
#end

cc = pickle.dumps(jobpath)
#print cc

tmp_file = open("output.txt","wb")
tmp_file.write(cc)
tmp_file.close()

