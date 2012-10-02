import os

from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'test_app.oauth.views.home', name='home'),
    url(r'^oauth2callback',
        'test_app.oauth.views.auth_return', name='auth_return'),
    # url(r'qrcode/(?P<key>.+)$', qrcode_view, name='qrcode'),
    # url(r'^test_app/', include('test_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'oauth/login.html'}),
    url(r'^api$', 'test_app.oauth.views.widget_process', name='api'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
    url(r'^accounts/login/$', 'django.contrib.auth.views.logout',
        {'template_name': 'oauth/logout.html'}, name='logout'),
)
