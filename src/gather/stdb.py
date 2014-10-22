# -*- coding: utf-8 -*-

import datetime
import os
from gather.job.models import Job, Scan


class dbpipe(object):
    def __init__(self):
        self.scan_id = 0
        self.job_id = None
        self.jobsetting = []
        self.cwd = os.getcwd()        
        if not os.path.isdir(self.cwd+"/localfiles"):
            os.mkdir(self.cwd+"/localfiles")
    
    def prepareScan(self,jobid):
        self.job_id = jobid
        job = Job.objects.get(pk=jobid)
        print job
        scan = Scan(job_id=jobid, scan_start=datetime.datetime.now(), scan_end=datetime.datetime.now())
        scan.save()
        self.scan_id = scan.id
        tmp_dts = job.get_rules
        if len(tmp_dts)>0:
            exec(tmp_dts)
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
