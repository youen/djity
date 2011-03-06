from django.conf.urls.defaults import *

urlpatterns = patterns('djity.simplepage.views',
	url(r'^$','page',{'module_name':'home'},name="simplepage-home-view"),
	url(r'^(?P<module_name>[-\w]+)/$','page',name="simplepage-view"),
)
