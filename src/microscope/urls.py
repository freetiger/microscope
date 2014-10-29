from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'microscope.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^job/', include('gather.job.urls', namespace="job")),
    url(r'^admin/', include(admin.site.urls)),
)
