# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: heyuxing
'''

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from gather.job.models import Job, Scan, ScanResult


# from django.http import HttpResponse
def index(request):
    job_list = Job.objects.all().order_by('-create_date')[:5]
    context = {'job_list': job_list}
    return render(request, 'index.html', context)
 
def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    context = {'job': job}
    return render(request, 'detail.html', context)
 
def results(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'results.html', {'job': job})

def saveOrUpdate(request, job_id):
    if job_id is not None:
        job = get_object_or_404(Job, pk=job_id)
    else:
        job = Job()
    if job is not Http404:
        job.job_name = request.POST['job_name']
#         job.get_rules = request.POST['get_rules']
#         job.keyword = request.POST['keyword']
#         job.thread_num = request.POST['thread_num']
        job.save()
        
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('job:detail', args=(job.id,)))
