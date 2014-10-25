# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: hyx
'''
from django.contrib import admin
from gather.job.models import Job,Scan

class ScanInline(admin.TabularInline):    #StackedInline
    model = Scan

class JobAdmin(admin.ModelAdmin):
    # ...
    list_display = ('job_name', 'job_flag', 'get_rules', 'searchwords', 'searchbase', 'create_date')
    #
    list_filter = ['create_date']
    search_fields = ['job_name']
    date_hierarchy = 'create_date'
    #
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['create_date'], 'classes': ['collapse']}),
    ]
    inlines = [ScanInline]
    
admin.site.register(Job, JobAdmin)