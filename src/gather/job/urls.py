# -*- coding: utf-8 -*-
'''
Created on 2014年10月20日

@author: heyuxing
'''

from django.conf.urls import patterns, url
from gather.job import views
urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<job_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<job_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
#     url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)


# from django.conf.urls import patterns, url
# from django.views.generic import DetailView, ListView
# from gather.job.models import Job,Scan,ScanResult
# 
# urlpatterns = patterns('',
#     url(r'^$',
#         ListView.as_view(
#             queryset=Job.objects.order_by('-create_date')[:5],
#             context_object_name='job_list',
#             template_name='gather/job/index.html'),
#         name='index'),
#     url(r'^(?P<pk>\d+)/$',
#         DetailView.as_view(
#             model=Job,
#             template_name='gather/job/detail.html'),
#         name='detail'),
#     url(r'^(?P<pk>\d+)/results/$',
#         DetailView.as_view(
#             model=Job,
#             template_name='gather/job/results.html'),
#         name='results'),
# #     url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='vote'),
# )