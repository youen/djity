from django.conf.urls.defaults import *

urlpatterns = patterns('djity.style.views',
        url('texture','texture',name='texture'),
        url('icons','icons',name='icons'),
        url('themeroller.html','themeroller',name="themeroller"),
        url('ui.css','css',{'template':'djity/style/jquery-ui.css'},name="ui_css"),
        url('project.css','css',{'template':'djity/style/project.css'},name="project_css"), 
        url('^(?P<template>[-\w]+)','css',name="generic_css"),
)
# place app url patterns here
