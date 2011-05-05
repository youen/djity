# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages
from django.conf import settings

from dajax.core import Dajax
from djity.utils.decorators import djity_view
from dajaxice.core import dajaxice_functions
from .models import Project, Member

register = lambda name:dajaxice_functions.register_function('djity.project.ajax',name)
@djity_view(perm='edit')
def save_tab_order(request,js_target,array,context=None):
    project = context['project']
    for module in  project.modules.all():
        module.tab_position = array.index(module.name)
        module.save()
register('save_tab_order')

@djity_view(perm='manage')
def edit_tab(request,js_target,label,status,context=None):
    module = context['module']
    module.label = label
    module.status = int(status)
    module.save()
register('edit_tab')

@djity_view(perm='edit')
def save_project_title(request,js_target,html,context=None):
    project = context['project']
    if html != '':
        project.label = html
        project.save()
        js_target.message(_('Project title saved.'))
register('save_project_title')

@djity_view(perm='edit')
def delete_tab(request,js_target,context=None):
    project = context['project']
    module = context['module']
    module.delete()
    if project.modules.count() == 0:
        url = project.parent.djity_url()
        project.delete()
    else:
        url = project.djity_url()

    js_target.redirect(url)
register('delete_tab')
    
@djity_view(perm='edit')
def get_module(request,js_target,context=None):
    out = ""
    project = context['project']
    for model in  project.get_available_modules():
        out += "<option value='%s'>%s</option>\n"%(model.__name__,model._meta.verbose_name)
    js_target.assign('#module_list','innerHTML',out)
    js_target.script("""
    $('#new_tab_name')
        .val($("#module_list option:selected").text())
        .select();
    """)

register('get_module')


@djity_view(perm='edit')
def add_module(request, js_target, tab_name, module_type, context=None):
    """
    Create a new tabulation in a project
    """
    from django.db.models import Max
    from django.db.models.loading import get_app
    from djity.utils.security import db_table_exists

    tables = [module_type.lower()+'_'+module_type.lower(),'djity_'+module_type.lower()+'_'+module_type.lower()]
    if not db_table_exists(tables):
        js_target.message(_("Tab creation failed. There is no table %s in the database, contact the administrator." % module_type))
        return

    try:
        model  = get_app(module_type.lower()).__getattribute__(module_type)
    except:
        model  = get_app('djity_'+module_type.lower()).__getattribute__(module_type)


    project=context['project']
    i = project.modules.aggregate(Max('tab_position'))['tab_position__max'] + 1
    if module_type == 'SimplePage':
        name = None
    else:
        name = module_type.lower() 

    module = model(
            project=project,
            name=name,
            label=tab_name,
            tab_position=i
        )
    module.save()
    
    js_target.redirect(module.djity_url(context))
register('add_module')


@djity_view(perm='manage')
def create_project(request,js_target,name,context=None):
    parent = context['project']
    child = Project(label=name,parent=parent)
    child.save(manager=context['user'])
    msg = _('Your new project %s was created !'%name)
    js_target.message(msg, post=True)
    js_target.redirect(child.djity_url())
register('create_project')

"""
@djity_view(perm='manage')
def module_visibility(request,visibility,context=None):
    module = context['module']
"""


@djity_view(perm='manage')
def save_manage_users(request,js_target,inherit,forbid,users=None,context=None):
    project = context['project']
    has_manager = False
    members = []
    deleted_members = []
    for user,role in users.items():
        if role == settings.MANAGER:
             has_manager = True
        member = Member.objects.get(project=project,user__username=user)
        if role == -1: #pseudo role for deleted user
             deleted_members.append(member)
        else:
            member.role = role
            members.append(member)
            
    if has_manager :
        for deleted_member in deleted_members:
            deleted_member.delete()
            msg = _('User %s is no longer a member of this project.'%user)
            js_target.message(msg)
            
        awaiting_members = 0
        for member in members:
            member.save()
            if member.role  == settings.AWAITING :
                awaiting_members += 1
            
        project.save()
        msg = _("Members of this project updated.")
        js_target.message(msg)
        js_target.close(awaiting_members)
        
    elif context['user'].username == user and role != settings.MANAGER:
        msg = _("You can't remove yourself from the managers of the current project.")
        js_target.message(msg)
        
    else:
        msg = _('At least one manager is required.')
        js_target.message(msg)


register('save_manage_users')

@djity_view(perm='manage')
def save_inherit_permissions(request, js_target,inherit,context=None):
    project = context['project']

    if inherit:
        if project.name == "root":
            msg = _("Root project can't inherit members.")
            js_target.message(msg)
            js_target.inherit_toggle(False)
            return 
        js_target.message(_(u'This project inherits members of %s project.'%project.parent.label))
    else:
        js_target.message(_(u"This project doesn't inherit members of %s project."%project.parent.label))

    project.inherit_members = inherit
    project.save()

register('save_inherit_permissions')

@djity_view(perm='manage')
def save_forbid_subscriptions(request, js_target,forbid,context=None):

    project = context['project']
    if forbid != project.forbid_subscriptions:
        project.forbid_subscriptions = forbid
        if forbid:
            js_target.message(_(u'New subscriptions to this project are now forbidden.'))
        else:
            js_target.message(_(u'New subscriptions to this project are now allowed.'))
        project.save()
        
register('save_forbid_subscriptions')

@djity_view(perm='manage')
def get_manage_users(request, js_target,context=None):
    project = context['project']
    context['roles'] = filter(lambda r:r[0] != 0 ,settings.ROLES_DISPLAY)
    context['members'] = project.members.all()
    context['inherit_members'] = map(lambda m:(m.user,settings.ROLES_DISPLAY[m.role][1]),project.get_members(inherit=True))
    context['users'] = [m.user for m in context['members']] 
    render = render_to_string("djity/project/manage_users.html",context)
    js_target.create_table(render)

register('get_manage_users')

@djity_view()
def project_subscribe(request,js_target,context=None):
    if context['project'].add_awaiting_user(context['user']):
        msg = _("Your subscription is registered. Wait for validation from a manager of this project.")
        js_target.message(msg,post=True)
    else:
        msg = _("You are no longer a member of this project.")
        js_target.message(msg,post=True)
    js_target.reload()

register('project_subscribe')

