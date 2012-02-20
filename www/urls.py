from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url('', include('gitaxis.urls')),
)
