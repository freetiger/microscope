# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''

from django.db import models

class Job(models.Model):
    job_name = models.CharField(max_length=256)
    job_flag = models.CharField(max_length=256)
    get_rules = models.TextField()
    searchwords = models.CharField(max_length=256)
    searchbase = models.CharField(max_length=256)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.job_name
    
class Scan(models.Model):
    job = models.ForeignKey(Job)
    scan_start = models.DateTimeField()
    scan_end = models.DateTimeField()
    scan_flag = models.CharField(max_length=256)
    is_finish = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.choice_text
    