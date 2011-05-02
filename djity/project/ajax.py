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
def save_tab_order(request,array,context=None):
    project = context['project']
    for module in  project.modules.all():
        module.tab_position = array.index(module.name)
        module.save()
    result =  Dajax()
    return result.json()
register('save_tab_order')

@djity_view(perm='manage')
def edit_tab(request,label,status,context=None):
    module = context['module']
    module.label = label
    module.status = int(status)
    module.save()
    result =  Dajax()
    return result.json()
register('edit_tab')

@djity_view(perm='edit')
def save_project_title(request,div_id,html,context=None):
    result =  Dajax()
    project = context['project']
    if html != '':
        project.label = html
        project.save()
        msg = unicode(_('Project title saved.'))
        result.script('message("%s")'%msg)
    return result.json()
register('save_project_title')

@djity_view(perm='edit')
def delete_tab(request,context=None):
    name = context['project_name']
    module = context['module']
    module.delete()
    dajax =  Dajax()
    dajax.redirect("/%s"%name)
    return dajax.json()
register('delete_tab')
    
@djity_view(perm='edit')
def get_module(request, context=None):
    dajax= Dajax()
    out = ""
    project = context['project']
    for model in  project.get_available_modules():
        out += "<option value='%s'>%s</option>\n"%(model.__name__,model._meta.verbose_name)
    dajax.assign('#module_list','innerHTML',out)
    dajax.script("""
    $('#new_tab_name')
        .val($("#module_list option:selected").text())
        .select();
    """)

    return dajax.json()
register('get_module')


@djity_view(perm='edit')
def add_module(request, tab_name, module_type, context=None):
    # build dictionary of classes available for modules
    from django.db.models import Max
    from django.db.models.loading import get_app
    try:
        model  = get_app(module_type.lower()).__getattribute__(module_type)
    except:
        model  = get_app('djity_'+module_type.lower()).__getattribute__(module_type)
    #bug context return tuple !
    project,=context['project'],
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
    
    dajax= Dajax()
    dajax.redirect(module.djity_url(context))
    return dajax.json()
register('add_module')


@djity_view(perm='manage')
def create_project(request,name,context=None):
    parent = context['project']
    child = Project(label=name,parent=parent)
    child.save(manager=context['user'])
    dajax = Dajax()
    msg = _(u'Your new project %s is created !'%name)
    messages.add_message(request, messages.INFO, unicode(msg) )
    dajax.redirect("/%s"%child.name)
    return dajax.json()
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

            for member in members: member.save()
            project.inherit_members = False
            project.save()
            msg = unicode(_(u"Members of this project updated"))
            js_target.message(msg)
            js_target.close()
        
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
def project_subscribe(request,context=None):
    dajax = Dajax()
    if context['project'].add_awaiting_user(context['user']):
        msg = unicode(_("Your subscription is registered. Wait for validation from a manager of this project."))
        messages.add_message(request, messages.INFO,msg)
    else:
        msg = unicode(_("You are no longer a member of this project."))
        messages.add_message(request, messages.INFO,msg)
    dajax.script('location.reload()')

    return dajax.json()
register('project_subscribe')

