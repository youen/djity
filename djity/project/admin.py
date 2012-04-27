from djity.project.models import Project,Member,Module
from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from djity.utils.decorators import djity_view
from django.contrib.contenttypes.models import ContentType

class DjityModelAdmin(admin.ModelAdmin):
    
    def __init__(self,*args,**kwarg):
        super(DjityModelAdmin,self).__init__(*args,**kwarg)
        self._project = self.admin_site._project
                
    def queryset(self, request):
        
        qs = super(DjityModelAdmin, self).queryset(request)
        return qs.filter(**self.objects_filter)
    
class ModuleModelAdmin(DjityModelAdmin):
    
    def __init__(self,*args,**kwarg):
        super(ModuleModelAdmin,self).__init__(*args,**kwarg)
        

        self.objects_filter = {
                               'project':self._project
                               }
    
class ProjectModelAdmin(DjityModelAdmin):
    
    def __init__(self,*args,**kwarg):
        super(ProjectModelAdmin,self).__init__(*args,**kwarg)
        

        self.objects_filter = {
                               'id':self._project.id
                               }
    
    

class DjityAdminSite(admin.AdminSite):
    
    def __init__(self,project):
        super(DjityAdminSite,self).__init__()
        self._project = project
        self._registery_by_name={}
        
    def register(self, model_or_iterable, admin_class=None, **options):
        super(DjityAdminSite,self).register( model_or_iterable, admin_class,**options)
        for model in self._registry:
            info = model._meta.app_label, model._meta.module_name
            self._registery_by_name['%s/%s'%info] = model
            
    def get_model_admin(self,name):
        return self._registry[self._registery_by_name[name]]
    
@djity_view()
def index(request,context=None, extra_context=None):
    return get_site(context["project"]).index(request,extra_context)

@djity_view()
def changelist_view(request,context=None, extra_context=None):
    path =  context['path']
    if path[-1] == "/":
        path = path[:-1]
    name = '/'.join(path.split('/')[-2:])
    return get_site(context["project"]).get_model_admin(name).changelist_view(request,extra_context)

@djity_view()
def add_view(request,context=None, extra_context=None):
    path =  context['path']
    if path[-1] == "/":
        path = path[:-1]
    name = '/'.join(path.split('/')[-3:-1])
    return get_site(context["project"]).get_model_admin(name).add_view(request,extra_context)

@djity_view()
def change_view(request,object_id,context=None, extra_context=None):
    path =  context['path']
    if path[-1] == "/":
        path = path[:-1]
    name = '/'.join(path.split('/')[-3:-1])
    return get_site(context["project"]).get_model_admin(name).change_view(request,object_id,extra_context)


@djity_view()
def history_view(request,object_id,context=None, extra_context=None):
    path =  context['path']
    if path[-1] == "/":
        path = path[:-1]
    name = '/'.join(path.split('/')[-4:-2])
    object_id = object_id.split('/')[-1]
    return get_site(context["project"]).get_model_admin(name).history_view(request,object_id,extra_context)

sites = {}
apps = []

def register(app,cls=DjityModelAdmin):
    apps.append((app,cls))

def get_site(project):
    if project not in sites:
        site = DjityAdminSite(project)
        for app,cls in apps:
            site.register(app, cls)
        sites[project] = site
    return sites[project]




def get_url():
    info = "project","project"
    urlpatterns = patterns(r'',
                           url(r'^$',
                               index,
                               name='index'),

                           )
    for model, model_admin in apps:

        info = model._meta.app_label, model._meta.module_name
    
        urlpatterns += patterns('',
            url(r'^%s/%s/$'%info,
                changelist_view,
                name='%s_%s_changelist' % info),
            url(r'^%s/%s/add/$'%info,
                add_view,
                name='%s_%s_add' % info),
            url(r'^(.+)/history/$',
                history_view,
                name='%s_%s_history' % info),
    #        url(r'^(.+)/delete/$',
    #            wrap(self.delete_view),
    #            name='%s_%s_delete' % info),
            url(r'^%s/%s/(.+)/$'%info,
                change_view,
                name='%s_%s_change' % info),
        )
    return urlpatterns


class ModuleInline(admin.TabularInline):
    model = Module

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ModuleInline,
    ]
  
class DjityProjectAdmin(ProjectAdmin,ProjectModelAdmin):
    pass

admin.site.register(Project,ProjectAdmin)
register(Project,DjityProjectAdmin)
