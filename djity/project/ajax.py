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
    name = context['project_name']
    module = context['module']
    module.delete()
    js_target.redirect("/%s"%name)
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
        js_target.message(_("Tab creation failed. No table for application, contact the administrator." % tables))
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
    msg = _(u'Your new project %s is created !'%name)
    js_target.message(msg, post=True)
    js_target.redirect("/%s"%child.name)
register('create_project')

"""
@djity_view(perm='manage')
def module_visibility(request,visibility,context=None):
    module = context['module']
"""


@djity_view(perm='manage')
def save_manage_users(request, js_target, inherit,users=None,context=None):
    project = context['project']
    if inherit:
        if project.name == "root":
            msg = unicode(_(u"Root project can't inherit members"))
            js_target.message(msg)
            return 
        project.inherit_members = True
        project.save()
        msg = unicode(_(u'This project inherit members of %s project.'%project.parent.label))
        js_target.message(msg)
        js_target.close()
        return

    else :
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
                msg = unicode(_(u'Member %s is no longer a member of this project.'%user))
                js_target.message(msg)
            
            awaiting_members = 0
            for member in members:
                member.save()
                if member.role  == settings.AWAITING :
                    awaiting_members += 1
            
            project.inherit_members = False
            project.save()
            msg = unicode(_(u"Members of this project updated"))
            js_target.message(msg)
            js_target.close(awaiting_members)
        
        elif context['user'].username == user and role != settings.MANAGER:
            msg = unicode(_(u"You can't change yourself your manager role."))
            js_target.message(msg)
        
        else:
            msg = unicode(_('At least one manager is required'))
            js_target.message(msg)


register('save_manage_users')

@djity_view(perm='manage')
def get_manage_users(request, js_target,context=None):
    project = context['project']
    context['roles'] = filter(lambda r:r[0] != 0 ,settings.ROLES_DISPLAY)
    context['members'] = project.get_members()
    context['users'] = [m.user for m in context['members']] 
    render = render_to_string("djity/project/manage_users.html",context)
    js_target.create_table(render)
    js_target.inherit_toggle(project.inherit_members)

register('get_manage_users')

@djity_view()
def project_subscribe(request,js_target,context=None):
    if context['project'].add_awaiting_user(context['user']):
        msg = unicode(_("Your subscription is registered. Wait for validation from a manager of this project."))
        messages.add_message(request, messages.INFO,msg)
    else:
        msg = unicode(_("You are no longer a member of this project."))
        messages.add_message(request, messages.INFO,msg)
    js_target.reload()

register('project_subscribe')

