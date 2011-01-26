from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages

from dajax.core import Dajax
from djity.core.project.decorators import check_perm_and_update_context
from dajaxice.core import dajaxice_functions
from .models import Project, Member, has_perm, get_role

register = lambda name:dajaxice_functions.register_function('djity.core.project.ajax',name)
@check_perm_and_update_context(perm='edit')
def save_tab_order(request,array,context=None):
    project = context['project']
    for module in  project.modules.all():
        module.tab_position = array.index(module.name)
        module.save()
    result =  Dajax()
    return result.json()
register('save_tab_order')

@check_perm_and_update_context(perm='edit')
def save_tab_name(request,label,context=None):
    module = context['module']
    module.label = label
    module.save()
    result =  Dajax()
    return result.json()
register('save_tab_name')

@check_perm_and_update_context(perm='edit')
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

@check_perm_and_update_context(perm='edit')
def delete_tab(request,context=None):
    name = context['project_name']
    module = context['module']
    module.delete()
    dajax =  Dajax()
    dajax.redirect("/%s"%name)
    return dajax.json()
register('delete_tab')
    
@check_perm_and_update_context(perm='edit')
def get_module(request, context=None):
    dajax= Dajax()
    out = ""
    project = context['project']
    for model in  project.get_availabe_modules():
        out += "<option value='%s'>%s</option>\n"%(model.__name__,model._meta.verbose_name)
    dajax.assign('#module_list','innerHTML',out)
    dajax.script("""
    $('#new_tab_name')
	    .val($("#module_list option:selected").text())
		.select();
    """)

    return dajax.json()
register('get_module')


@check_perm_and_update_context(perm='edit')
def add_module(request, tab_name, module_type, context=None):
    # build dictionary of classes available for modules
    from django.db.models import Max
    from django.db.models.loading import get_app
    model  = get_app(module_type.lower()).__getattribute__(module_type)
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


@check_perm_and_update_context(perm='manage')
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

@check_perm_and_update_context(perm='manage')
def manage_users(request,target,users=None,context=None):
    project = context['project']
    dajax = Dajax()
    if users:
        has_manager = False
        members = []
        deleted_members = []
        for user,role in users.items():
            if role == 'manager':
                has_manager = True

            member = Member.objects.get(project=project,user__username=user)
            if role == 'deleted':
                deleted_members.append(member)


            else:
                role = project.role_set.get(name=role)
                member.role = role
                members.append(member)
            
        if has_manager :
            for deleted_member in deleted_members:
                deleted_member.delete()
                msg = unicode(_(u'Member %s is no longer a member of this project.'%user))
                dajax.script('message("%s")'%msg)

            for member in members: member.save()
            msg = unicode(_(u"Members of this project updated"))
            dajax.script('message("%s")'%msg)
            dajax.script('manage_users_dialog_close()')
            return dajax.json()
        
        elif context['user'].username == user and role != 'manager':
            msg = unicode(_(u"You can't change yourself your manager role."))
            dajax.script(u'manage_users_dialog_error("%s")'%msg)
            return dajax.json()
        
        else:
            message = _('At least one manager is required')
            return dajax.json()


    context['roles'] = filter(lambda r:r.name not in ['anyone','anonymous'],project.role_set.all())
    context['members'] = Member.objects.filter(project=project)
    context['users'] = [m.user for m in context['members']] 
    render = render_to_string("core/projects/manage_user.html",context)
    dajax.assign(target,'innerHTML',render)
    dajax.script('manage_users_dialog_widgetify()')

    return dajax.json()
register('manage_users')

@check_perm_and_update_context(perm='manage')
def project_visibility(request,visibility,context=None):
    dajax = Dajax()
    context['project'].set_visibility(visibility)
    msg = unicode(_("The current project is now %s"%visibility))
    messages.add_message(request, messages.INFO,msg)
    dajax.script('location.reload()')
    return dajax.json()
register('project_visibility')

@check_perm_and_update_context()
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

