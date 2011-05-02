from django.utils.translation import ugettext_lazy as _ 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.conf import settings

from djity.portal.models import SiteRoot
from djity.portlet.models import TextPortlet
from djity.transmeta import TransMeta
from djity.utils import has_perm, granted_perms
from djity.utils.inherit import SuperManager


class Project(models.Model):
    """
    A class for independant projects in Djity Portal, with users, permissions,
    installed modules, etc...
    """

    __metaclass__ = TransMeta

    name = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="")
    created_on = models.DateTimeField(auto_now=True)
    is_root = models.BooleanField(default=False)
    inherit_members = models.BooleanField(default=False)
    parent = models.ForeignKey('self',related_name="children",null=True,default=None) 
    css = models.OneToOneField('style.CSS')

    class Meta :
        translate = ('label','description')

    def init_modules(self,modules=None):
        """
        Initialize modules of a new project
        """
        # modules to activate can either be given as parameter or fetched from settings
        if not modules:
            from django.conf import settings
            modules = settings.DEFAULT_PROJECT_MODULES
        
        from django.utils.importlib import import_module
        for i, (module , name)  in enumerate(modules):
            djity_module = import_module(module).djity_module
            model = getattr(import_module('%s.models'%module),djity_module)

            try:
                Module.objects.get(project=self,name=name)
            except:
                model(project=self,name=name,label=name,tab_position=i,status=settings.DRAFT).save()

    def save(self,*args,**kwargs):
        """
        If a project is new initialize all its dependances
        """
        # Is the project new ?
        new = False
        if self.id == None:
            new = True

        # to do before saving
        if new:
            if 'manager' in kwargs:
                user = kwargs['manager']
                del kwargs['manager']
            else:
                # Get superuser
                user = User.objects.get(is_superuser=True)
            
            if not self.name:
                self.name = slugify(self.label)

            from djity.style.models import CSS
            css = CSS()
            css.save()
            self.css = css

        super(Project,self).save(*args, **kwargs)

        # todo after saving
        if new:

            # Set current user as manager of the new project
            Member(project=self,user=user,role=settings.MANAGER).save()
            self.init_modules()
            
            #add a footer portlet
            TextPortlet(content="This is a project footer. Edit me !",
                    div_id="footer",container=self,position="bottom",
                    rel_position=0).save()
            
    def __unicode__(self):
        return self.label

    def get_parents(self):
        """
        Get the hierarchy of parent projects
        """
        if self.parent:
            parents = self.parent.get_parents()
            parents += [self.parent]
        else:
            parents = []
        return parents

    def get_members(self):
        """
        Return the members of this project.
        If this project inherit permissions return the members for the parent project.
        """
        if self.inherit_members: 
            return self.parent.get_members()
        else:
            return  Member.objects.filter(project=self)     

    def get_role(self,user):
        """
        Return the role for the user `user` of this project.
        If `user` is anonymous or `user` haven't role for this project, return the anonymous role.
        If this project inherit permissions return the role for the parent project.
        """
        if self.inherit_members: 
            return self.parent.get_role(user)
        else:
            # attempt to get the role of the user
            try:
                if user.is_anonymous():
                    return settings.ANONYMOUS
                else:
                    return  Member.objects.get(user=user,project=self).role     
            except Member.DoesNotExist:
                return settings.ANONYMOUS

    def can_view(self,user):
        """
        check if a user can view a project,
        used to build parent hierarchy in update_context,
        we consider that a user can view a project if he can view at least 
        one of its modules
        """
        role = self.get_role(user)
        for module in self.modules.all():
            if has_perm('view',role,module.status):
                return True
        return False

    def update_context(self,context):
        """
        Get context for all project templates or sub templates
        """ 
        # Get site level context
        SiteRoot.objects.get(label='home').update_context(context)
      
        # Fetch the role of the current user in this project
        context['role'] = self.get_role(context['user'])
        
        # Create dictionary of modules connected and their subnavigation menu,
        # and a list of the module tabs according to the role of the user
        # and check if the required permission is granted on the current module
        context['module_tabs'] = []
        for module in self.modules.order_by('tab_position'):
            name = module.name
            if name == context['module_name']:
                context['module'] = module
                context['perm'] = granted_perms(context['role'],module.status)
                context['tab_status'] = module.status
                context['status_display'] = settings.STATUS_DISPLAY
            if has_perm('view',context['role'],module.status):
                context['module_tabs'].append(name)
                context["%s_tab_display"%name] = module.label.capitalize()
                context["%s_tab_url"%name] = module.djity_url(context)

        # if no module name is declared we are in the project's context
        # for example the request might be for project.css
        # in this case permissions are asked for a current status of public
        if context['module_name'] is None:
            context['perm'] = granted_perms(context['role'],settings.PUBLIC)

        # get hierarchy of parent projects
        context['parent_projects'] = filter(lambda p:p.can_view(context['user']) ,self.get_parents())
        context['children_projects'] = filter(lambda p:p.can_view(context['user']) ,self.children.all())
    
    def get_available_modules(self):
        """
        get the list of modules avaible for this project
        """
        from djity.simplepage.models import SimplePage
        from djity.utils import djity_modules

        result = [SimplePage]
        installed_modules_name  = [module.name for module in self.modules.all() ]

        for model in djity_modules():
                if model.__name__.lower() not in installed_modules_name:
                    result.append(model)
        return result

    def add_awaiting_user(self,user,remove_if_exist=True):
        """
        add a user awaiting validation
        """
        try:
            member = Member.objects.get(project=self,user=user)
            member.delete()
            return False
        except Member.DoesNotExist:
            Member(project=self,user=user,role=settings.AWAITING).save()
            return True

class Member(models.Model):
    """
    A member of a project in Djity's forge
    """
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User,related_name="project_memberships")
    role = models.IntegerField()

    def __unicode__(self):
        return "%s: %s of %s" % (self.user,self.role,self.project)

    class Meta:
        unique_together = ('user','project')

class Module(models.Model):
    
    __metaclass__ = TransMeta

    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    objects = SuperManager()

    name =  models.SlugField(_('Module name'),max_length=50)
    project = models.ForeignKey('Project', related_name='modules')
    tab_position = models.IntegerField('Tab position')
    label = models.CharField(_('Label'),max_length=200,
                help_text = _('the label view in tabs')
            )
    status = models.IntegerField(default=settings.DRAFT)

    module_label = _('Module')

    class Meta:
        translate = ('label',)
        unique_together = ('name','project')
   

    def url(self):
        return self.module.url(self.project.name)

    def save(self,*args,**kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)

        if not self.name:
            self.name = slugify(self.label)

        super(Module,self).save(*args,**kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Module):
            return self
        return model.objects.get(id=self.id)


    def __unicode__(self):
        return "Module: %s" % self.label

###
# Define exceptions
###

class ModuleNotConnectedException(Exception):
    pass

