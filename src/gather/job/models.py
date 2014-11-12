# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''

from django.db import models
import re

class Job(models.Model):
    job_name = models.CharField(max_length=256, verbose_name='任务名称')
    get_rules = models.TextField(verbose_name='任务规则')
    placeholders = models.CharField(max_length=256, blank=True, verbose_name='规则占位符')
    thread_num = models.IntegerField(default=1, verbose_name='并发线程数')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    
    def placeholders_tips(self):
        tips=[]
        placeholders_regular = re.compile(r'\{\{([^}]*)\}\}')
        placeholders = placeholders_regular.findall(self.get_rules)
        
        for placeholder in placeholders:
            tips.append(placeholder)
        return tips
    
    def __unicode__(self):
        return self.job_name
    
    class Meta:
        ordering = ['job_name']
    
class Scan(models.Model):
    job = models.ForeignKey(Job)
    scan_start = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    scan_end = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    is_finish = models.CharField(default=0, max_length=256, verbose_name='是否完成')
    
    def __unicode__(self):
        return self.job.job_name
    
    class Meta:
        ordering = ['scan_start']

class ScanResult(models.Model):
    scan = models.ForeignKey(Scan)
    scan_result = models.TextField()
    
    def __unicode__(self):
        return self.scan_result
    