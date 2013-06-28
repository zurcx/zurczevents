#encoding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('events.views',
    url(r'^$', 'index', name='events'),
    url(r'^(?P<pk>\d+)/$', 'details', name='events_details'),
    url(r'^novo-evento/$', 'create', name='events_create'),
    url(r'^meus-eventos/$', 'my', name='events_my'),
    url(r'^(?P<pk>\d+)/alterar/$', 'edit', name='events_edit'),
    url(r'^(?P<pk>\d+)/apagar/$', 'delete', name='events_delete'),
    url(r'^(?P<pk>\d+)/albuns/$', 'albums', name='events_albums'),
    url(r'^(?P<pk>\d+)/albuns/criar/$', 'create_album', 
        name='events_create_album'),
)