from django.conf.urls.defaults import *

urlpatterns = patterns('djity.simplepage.views',
	url(r'^(?P<module_name>[-\w]+)/*$','page',name="simplepage-view"),
)
