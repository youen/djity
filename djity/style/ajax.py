from django.conf import settings
from django.template.loader import render_to_string
from dajax.core import Dajax
from djity.project.decorators import check_perm_and_update_context
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages


from dajaxice.core import dajaxice_functions
register = lambda name:dajaxice_functions.register_function('djity.style.ajax',name)

"""
@check_perm_and_update_context(perm='manage')
def edit_project_style(request,target,context=None):
    dajax = Dajax()
    project = context['project']
    css = project.css

    css_context = css.get_context()

    edit_style_content = []
    for group,items in settings.EDIT_STYLE_ORDER:
        content_items = []
        for item in items:
            content_items.append((item[0],item[1],css_context[item[1]],item[1].split('_')[-1]))
        edit_style_content.append((group,content_items))

    context['edit_style_content'] = edit_style_content

    render = render_to_string("core/style/edit.html",context)
    dajax.assign(target,'innerHTML',render)
    dajax.script("project_style_dialog_widgetify()")
    return dajax.json()
"""

@check_perm_and_update_context(perm='manage')
def save_project_style(request,style_values,context=None):
    dajax = Dajax()
    project = context['project']
    css = project.css
    css.__dict__.update(style_values)
    css.save()
    message = _("The style of the project has been saved")
    messages.add_message(request, messages.INFO, unicode(message))
    return dajax.json()

register('save_project_style')

@check_perm_and_update_context(perm='manage')
def download_params(request,js_target,context=None):
    js_target.val(context['project'].css.serialize())

register('download_params')


@check_perm_and_update_context(perm='manage')
def inherit_style(request,js_target,context=None):

    project = context['project']

    if project.parent:
        project.css.set_all_values(project.parent.css.get_context())
        project.css.save()
        js_target.message(unicode(_("Style of the current project has been overwritten by the style of its parent \"%s\"" % project.parent.name)),post=True)
        js_target.reload()
    else:
        js_target.message(unicode(_("The current project is root and cannot inherit its style")))

register('inherit_style')
