from django.conf.urls.defaults import *

urlpatterns = patterns('djity.simplepage.views',
	url(r'^$','page',{'module_name':'home'},name="simplepage-home-view"),
	url(r'^/edit$','edit',{'module_name':'home'},name="simplepage-home-edit"),
	url(r'^/draft$','draft',{'module_name':'home'},name="simplepage-home-draft"),
	url(r'^(?P<module_name>[-\w]+)/$','page',name="simplepage-view"),
	url(r'^(?P<module_name>[-\w]+)/edit$','edit',name="simplepage-edit"),
	url(r'^(?P<module_name>[-\w]+)/publish$','publish',name="simplepage-edit"),
	url(r'^(?P<module_name>[-\w]+)/draft$','draft',name="simplepage-draft"),
)
