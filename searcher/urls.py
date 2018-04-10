from django.conf.urls import url

from . import views


app_name = 'searcher'
urlpatterns  = [
    url(r'^searcher-admin/login$', views.login_view, name='login'),
    url(r'^searcher-admin/logut$', views.logout_view, name='logout'),
    url(r'^searcher-admin$', views.view_folder, name='view_folder'),
    url(r'^searcher-admin/(?P<current_folder_id>[0-9]*)$', views.view_folder, name='view_folder'),
    url(r'^searcher-admin/(?P<folder_id>[0-9]+)/change$', views.change_folder, name='change_folder'),
    url(r'^searcher-admin/file/(?P<file_id>[0-9]+)/change$', views.change_file, name='change_file'),
    url(r'^searcher-admin/search$', views.search, name='search'),
    url(r'^search_ajax/$', views.search_ajax, name='search_ajax'),
    url(r'^search$', views.user_search, name='user_search'),
]