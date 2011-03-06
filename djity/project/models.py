from django.utils.translation import ugettext_lazy as _ 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

from djity.portal.models import SiteRoot
from djity.portlet.models import update_portlets_context, TextPortlet
from djity.transmeta import TransMeta
from djity.utils.inherit import SuperManager

class Project(models.Model):
    """
    A developement and documentation project model for Djity's forge
    """

    __metaclass__ = TransMeta

    name = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="")
    created_on = models.DateTimeField(auto_now=True)
    is_root = models.BooleanField(default=False)
    parent = models.ForeignKey('self',related_name="children",null=True,default=None) 
    css = models.OneToOneField('style.CSS')

    PARSER_CHOICES = (
            ('h',_('Html')),
            ('c',_('Creole')), 
            ('t',_('Textile')),
            ('m',_('Markdown')),
            ('r',_('ReStruturedText')), #TODO: find a RST widget
            )

    parser = models.CharField(max_length=1,
                        choices= PARSER_CHOICES,
                        default='c',
                        blank=False, null=True, 
                        verbose_name=_('Wiki syntax parser'))

    class Meta :
        translate = ('label','description')

    def init_permissions(self,creator):
        """
        Initialize first member, default roles and permissions 
        """
        from django.conf import settings

        # Create default roles as defined in settings.py
        for role in settings.DEFAULT_ROLES:
            Role(name=role[0],description=role[1],project=self).save()

        # Create generic roles
        manager = Role(name='manager',description="Project manager",project=self)
        manager.save()
        Role(name='anonymous',description="Anyone including anonymous",project=self).save()
        Role(name='awaiting',description="Users awaiting validation",project=self).save()

        # Create default permissions as defined in settings.py
        project_roles = dict([(role.name,role) for role in  Role.objects.filter(project=self)])

        for permission,(description,roles) in settings.DEFAULT_PERMISSIONS.iteritems():
            p = Permission(name=permission, description=description, project=self)
            p.save()
            if 'anyone' in roles:
                for role in project_roles.values():
                    p.authorized_roles.add(role)
            else:
                for role in roles:
                    p.authorized_roles.add(project_roles[role])
        
        # Set current user as manager of the new project
        Member(project=self,user=creator,role=manager).save()

    @property
    def is_public(self):
        """
        Check if the project is viewable by anonymous users
        """ 
        public = Role.objects.get(project=self,name='anonymous')
        view_perm = Permission.objects.get(project=self,name='view')
        return public in view_perm.authorized_roles.all()

    def set_visibility(self,visibility='private'):
        """
        set visibility to public or private
        """
        public = Role.objects.get(project=self,name='anonymous')
        view_perm = Permission.objects.get(project=self,name='view')
        roles = view_perm.authorized_roles
        if visibility == 'public':
            if public not in roles.all():
                roles.add(public)
        else:
            if public in roles.all():
                roles.remove(public)

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
                model(project=self,name=name,label=name,tab_position=i).save()

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

            # Init permissions with superuser as manager (should be a parameter
            # later on)
            self.init_permissions(user)
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

    def update_context(self,context):
        """
        Get context for all project templates or sub templates
        """
        # Get site level context
        SiteRoot.objects.get(label='home').update_context(context)
        # Add project level context
        context.update({
            'project_name':self.name,
            'parser':self.parser,
        })
        
        # Create dictionary of modules connected and their subnavigation menu
        module_tabs = []
        for module in self.modules.order_by('tab_position'):
            module_tabs.append(module.name)
            context["%s_tab_display"%module.name] = module.label.capitalize()
            context["%s_tab_url"%module.name] = module.djity_url(context)
        context["module_tabs"] = module_tabs

        # Add context of project level portlets
        update_portlets_context(self,context)

        #permission 
        context['perm'] = {}
        for perm in filter(lambda x:x.is_authorized(context['role']),self.permission_set.all()):
            context['perm'][perm.name] = perm

        # get hierarchy of parent projects
        context['parent_projects'] = filter(lambda p:has_perm(p,context['user'],'view') ,self.get_parents())
        context['children_projects'] = filter(lambda p:has_perm(p,context['user'],'view') ,self.children.all())
    
    def get_availabe_modules(self):
        """
        get the list of modules avaible for this project
        """
        from djity.simplepage.models import SimplePage
        from djity.utils import djity_modules

        result = [SimplePage]
        instaled_modules_name  = [module.name for module in self.modules.all() ]

        for model in djity_modules():
                if model.__name__.lower() not in instaled_modules_name:
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
            awaiting = Role.objects.get(project=self,name='awaiting')
            Member(project=self,user=user,role=awaiting).save()
            return True

        
class Version(models.Model):
    """
    A planned version of a project
    """
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(default="")
    deadline = models.DateTimeField()

    def __unicode__(self):
        return self.name 

class Role(models.Model):
    """
    Model for available roles of projects' members
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.name 

class Member(models.Model):
    """
    A member of a project in Djity's forge
    """
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User,related_name="project_memberships")
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return "%s: %s of %s" % (self.user,self.role,self.project)

    class Meta:

        unique_together = ('user','project')

class Permission(models.Model):
    """
    Permissions are queried by projects's modules and are associated to a project and its users' roles
    """
    name = models.CharField("name",max_length=200)
    description = models.TextField("description")
    project = models.ForeignKey(Project)
    authorized_roles = models.ManyToManyField(Role)

    def is_authorized(self,role):
        """
        Is a role authorized to access this permission ?
        """
        # Get authorized roles
        authorized_roles = self.authorized_roles.all()

        # If public is in authorized_roles always accept permission
        if role in authorized_roles:
            return True


        # manager has all permissions
        if role.name == 'manager':
            return True



    def user_is_authorized(self,user):
        """
        Is a user authorized to access this permission ?
        """
        # Get generic roles
        anonymous = Role.objects.get(project=self.project,name='anonymous')
        manager = Role.objects.get(project=self.project,name='manager') 
    
    
        # Get authorized roles
        roles = self.authorized_roles.all()
    
        # If public is in authorized_roles always accept permission
        if anonymous in roles:
            return True

        if user.is_anonymous():
            return False

        # attempt to get the role of the user
        try:
            user_role = Member.objects.get(user=user,project=self.project).role
        except Member.DoesNotExist:
            return False
    
        # manager has all permissions
        if manager == user_role:
            return True
    
    
        # Finally check if the user's role was explicitly authorized
        return user_role in roles


    def __unicode__(self):
        return self.name

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
    is_active = models.BooleanField( _('is active'),
        default=True,
        help_text=_("if disabled, this module won't appear in the project")
        )

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

class ModuleNotActiveException(Exception):
    pass

###
# Define functions used by modules views to check the validity of a request
###
def get_context(project_name,module_name,user):
    """
    Test for a project if module module_name is active 
    and return the project, instance of this module for this project and the context
    """
    try:
        project = Project.objects.get(name=project_name)
        module = Module.objects.get(name=module_name,project=project).as_leaf_class()
    except:
        raise ModuleNotConnectedException()
    if module.is_active:
        context = project.get_context()
        context = get_portlets_context(module,context)
        context['project'] = project
        context['module'] = module
        return context
    else:
        raise ModuleNotActiveException(_(u'%s is not active')%mc)

def is_active(project,module_name):
    """
    Check if a module is registered in a project
    """
    # If module instance doesn't exist return false
    try:
        module = Module.objects.get(name=module_name,project=project)
    except:
        return False

    # Otherwise, ok this module is registered on this project 
    return module.is_active

def has_perm(project,user,permission_name):
    """
    Check if a user has a permission on a project
    """
    try:
        perm = Permission.objects.get(project=project,name=permission_name)
    except:
        return False
    
    return perm.user_is_authorized(user)

def get_role(project,user):
    try:
       role = Member.objects.get(user=user,project=project).role
    except:
        return None

    return role
    