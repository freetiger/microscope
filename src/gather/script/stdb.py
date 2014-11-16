# -*- coding: utf-8 -*-

import datetime
import os
from gather.job.models import Job, Scan
import MySQLdb

def getConnect():
    host = 'localhost'
    port = 3306
    database = 'microscope'
    user = 'hyx1161'
    password = '1161hyx'
    charset="utf8"
    return MySQLdb.connect(host=host, port=port, db=database,user=user,passwd=password,charset=charset)

def saveScanResult(scan_id=0, scan_result=""):
    conn = getConnect()
    cur = conn.cursor()
    cur.execute("insert into job_scanresult(scan_id,scan_result) values (%s,%s)" , (int(scan_id), str(scan_result)))
    conn.commit()
    conn.close()

class dbpipe(object):
    def __init__(self):
        self.scan_id = 0
        self.job_id = None
        self.jobsetting = []
        self.cwd = os.getcwd()        
        if not os.path.isdir(self.cwd+"/localfiles"):
            os.mkdir(self.cwd+"/localfiles")
    
    def prepareScan(self,jobid, placeholders={}):
        self.job_id = jobid
        job = Job.objects.get(pk=jobid)
        print job
        scan = Scan(job_id=jobid, scan_start=datetime.datetime.now(), scan_end=datetime.datetime.now())
        scan.save()
        self.scan_id = scan.id
        rules = job.get_rules
        #传入的参数覆盖数据库中的数值
        if len(job.placeholders)>0:
            temp_placeholders = eval(job.placeholders)
            for placeholder_key in placeholders:
                temp_placeholders[placeholder_key] = placeholders[placeholder_key]
        else:
            temp_placeholders = placeholders
        #
        if len(rules)>0:
            for placeholder_key in temp_placeholders:
                rules = rules.replace("{{"+placeholder_key+"}}",temp_placeholders[placeholder_key])
            exec(rules)
            self.jobsetting = eval("jobpath")
            
        return 0

    def finishscan(self):
        scan = Scan.objects.get(pk=self.scan_id)
        scan.scan_end=datetime.datetime.now()
        scan.is_finish = '1'
        scan.save()
        return 0
        
if __name__ == "__main__" :
    pass