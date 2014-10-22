# -*- coding: utf-8 -*-
import getopt
import sys

import django

from grabber import Grabber


help_text="""Usage: python wg_jshell.py [options]

Options:
  -j ..., --jobid=...              the jobid
  -h, --help                       show this help

Examples:
  wg_jshell.py --jobid=1     scan the job with the id 1
"""
def print_help():
    print >>sys.stderr, help_text
    sys.exit(1)

#启动抓取任务的操作菜单
def main(args):
    
    try:                                
        opts, args = getopt.getopt(args, "hj:n:", ["help", "jobid=", "keyword="])
    except getopt.GetoptError:
        print_help()
        
    job_id = 421
    keyword = None
    
    for opt, arg in opts:
        
        if opt in ("-h", "--help"):
            print_help()
        elif opt in ("-j", "--jobid"):
            try:
                job_id=int(arg)
            except:
                print "jobid must be interger"
        elif opt in ("-n", "--keyword"):
            keyword = arg
            #.replace("-","%")   
    the_grabber = Grabber()
    thread_num=1
    the_grabber.startscan(job_id,keyword, thread_num)
    
   

if __name__ == '__main__':    
    django.setup()
    main(sys.argv[1:])

