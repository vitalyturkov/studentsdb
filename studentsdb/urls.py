"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include, patterns
from django.contrib import admin
from students.views.contact_admin import ContactView
from students.views.students import StudentUpdateView, StudentCreateView, StudentDeleteView
from students.views.groups import GroupCreateView, GroupUpdateView, GroupDeleteView
from students.views.journal import JournalView
from .settings import MEDIA_ROOT, DEBUG



urlpatterns = [
	#students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$', StudentCreateView.as_view(),
	name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
	name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$',StudentDeleteView.as_view(),
	name='students_delete'),
	
	#groups urls
    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),  
    url(r'^groups/add/$', GroupCreateView.as_view(), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$',GroupUpdateView.as_view(),
	name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$',GroupDeleteView.as_view(),
	name='groups_delete'),
	
    #journal urls
    url(r'^journal/$', JournalView.as_view(), name='journal'),
    url(r'^journal/stud_(?P<spk>\d+)?/?$', JournalView.as_view(), name='stud_journal'),
    url(r'^journal/group_(?P<gpk>\d+)?/?$', JournalView.as_view(), name='group_journal'),


    #exams
    url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
    url(r'^exams/add/$', 'students.views.exams.exams_add', name='exams_add'),
    url(r'^exams/(?P<eid>\d+)/edit/$','students.views.exams.exams_edit',
    name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/delete/$','students.views.exams.exams_delete',
    name='exams_delete'),

    #contact Admin Form
    url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),

    url(r'^admin/', include(admin.site.urls)),
  

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT})
]


if DEBUG:
# serve files from media folder
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': MEDIA_ROOT}))
