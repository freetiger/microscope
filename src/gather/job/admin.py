# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''
from django.contrib import admin
from gather.job.models import Job,Scan,ScanResult

class ScanInline(admin.TabularInline):    #StackedInline
    model = Scan
    extra = 0

class JobAdmin(admin.ModelAdmin):
    # ...
    list_display = ('job_name', 'get_rules', 'keyword', 'thread_num', 'create_date')
    #
    list_filter = ['create_date']
    search_fields = ['job_name']
    date_hierarchy = 'create_date'
    inlines = [ScanInline]
    
class ScanResultInline(admin.TabularInline):    #StackedInline
    model = ScanResult
    extra = 0
    
class ScanAdmin(admin.ModelAdmin):
    # ...
    #list_display = ('job_name', 'get_rules', 'keyword', 'thread_num', 'create_date')
    #
#     list_filter = ['create_date']
#     search_fields = ['job_name']
#     date_hierarchy = 'create_date'
    inlines = [ScanResultInline]
    
admin.site.register(Job, JobAdmin)
admin.site.register(Scan, ScanAdmin)