# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''

from django.db import models

class Job(models.Model):
    job_name = models.CharField(max_length=256)
    get_rules = models.TextField()
    keyword = models.CharField(max_length=256, blank=True)
    thread_num = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.job_name
    
class Scan(models.Model):
    job = models.ForeignKey(Job)
    scan_start = models.DateTimeField()
    scan_end = models.DateTimeField(blank=True)
    is_finish = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.job.job_name

class ScanResult(models.Model):
    scan = models.ForeignKey(Scan)
    scan_result = models.TextField()
    
    def __unicode__(self):
        return self.scan_result
    