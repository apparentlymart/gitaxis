from django.conf.urls.defaults import patterns, include, url

from os.path import join, dirname

repo_urlpatterns = patterns('gitaxis.views',
    url(
        '^branches/(?P<branch_name>[^/]+)$',
        'repo_branch_detail',
        name="repo_branch_detail"
    ),
    url(
        '^commits/(?P<branch_name>[^/]+)$',
        'repo_commit_detail',
        name="repo_commit_detail"
    ),
)

reposet_urlpatterns = patterns('gitaxis.views',
    url(
        '^(?P<repo_name>[^/]+)$',
        'repo_detail',
        name="repo_detail"
    ),
    url(
        '^(?P<repo_name>[^/]+)/',
        include(repo_urlpatterns),
    ),
)

urlpatterns = patterns('gitaxis.views',
    url(
        '^$',
        'index',
        name="index"
    ),
    url(
        '^~(?P<username>[^/]+)/',
        include(reposet_urlpatterns),
    ),
    url(
        '^',
        include(reposet_urlpatterns),
    ),
)

urlpatterns += (
    url(
        r'^:static/(?P<path>.*)$',
        'django.views.static.serve',
        { 'document_root': join(dirname(__file__), 'static') },
        name='static'
    ),
)
