# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''

from django.db import models

class Job(models.Model):
    job_name = models.CharField(max_length=256, verbose_name='任务名称')
    get_rules = models.TextField(verbose_name='任务规则')
    keyword = models.CharField(max_length=256, blank=True, verbose_name='规则关键字')
    thread_num = models.IntegerField(default=1, verbose_name='并发线程数')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    
    def __unicode__(self):
        return self.job_name
    
    class Meta:
        ordering = ['job_name']
    
class Scan(models.Model):
    job = models.ForeignKey(Job)
    scan_start = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    scan_end = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    is_finish = models.CharField(max_length=256, verbose_name='是否完成')
    
    def __unicode__(self):
        return self.job.job_name
    
    class Meta:
        ordering = ['scan_start']

class ScanResult(models.Model):
    scan = models.ForeignKey(Scan)
    scan_result = models.TextField()
    
    def __unicode__(self):
        return self.scan_result
    