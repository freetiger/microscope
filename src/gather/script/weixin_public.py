# -*- coding: utf-8 -*-
'''
Created on 2015年1月12日

@author: heyuxing
'''
from gather.job.models import Job
from gather.script.grabber import Grabber
from gather.script import utils
import re


'''
http://weixin.sogou.com 搜索的结果页的页数，并不准确，需要逼近最后一页确定总页数
'''
def get_page_total():
    page_total = 1
    page_current = 1
    param_retrieve_str = re.compile(r'"totalPages":(\d*),"page":(\d*)')
    while True:
        page_src = utils.getUrlContent("http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page="+str(page_current))
        params = param_retrieve_str.findall(page_src)
        print params
        page_total = int(params[0][0])
        page_current = int(params[0][1])
        if(page_current>=page_total):
            break
        else:
            page_current = page_total
        
    return page_total     

def gen_list_page(base_url, page_total=1):
    list_page = "inline:///"
    for index in range(page_total):
        list_page = list_page+";"+base_url+str(index+1)
    return list_page

def scan_weixin_public():
    job_id = 5
    job = Job.objects.get(pk=job_id)
    if job is not None:
        job_name = job.job_name
        get_rules = job.get_rules
        placeholders = {}
        thread_num = 1
        #
        base_url = "http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page="
        list_page = gen_list_page(base_url, get_page_total())
        print "list_page="+list_page
        print "toalt="+str(get_page_total())
        get_rules = get_rules.replace("{{list_page}}", list_page)
        print get_rules
        Grabber().startscan(job_id=job_id, job_name=job_name, get_rules=get_rules, placeholders=placeholders, thread_num=thread_num)


if __name__ == "__main__":   
        base_url = "http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt-Atb62Noyz4nKX1nvrmFHQ&page="
        list_page = gen_list_page(base_url, get_page_total())
        print "list_page="+list_page
        print get_page_total()
    