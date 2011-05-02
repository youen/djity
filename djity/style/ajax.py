import json
from django.conf import settings
from django.template.loader import render_to_string
from dajax.core import Dajax
from djity.utils.decorators import djity_view
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages


from dajaxice.core import dajaxice_functions
register = lambda name:dajaxice_functions.register_function('djity.style.ajax',name)

@djity_view(perm='manage')
def save_project_style(request,style_values,js_target,context=None):
    if style_values.__class__.__name__ in ['unicode','str']:
        # style can be given as string in json
        try:
            style_values = json.loads(style_values)
        except:
            style_values = {}
        
    if style_values.__class__.__name__ == 'list':
        # style can be given as a list of tuples
        style_values = dict(style_values)

    context['project'].css.set_all_values(style_values)
    message = _("The style of the project has been saved")
    js_target.message(message,post=True)
    js_target.reload()

register('save_project_style')

@djity_view(perm='manage')
def download_params(request,js_target,context=None):
    js_target.val(json.dumps(context['project'].css.get_values()))

register('download_params')

@djity_view(perm='manage')
def set_default(request,js_target,context=None):
    context['project'].css.set_to_default()
    message = _("The style of the project has been set to default")
    js_target.message(message,post=True)
    js_target.reload()

register('set_default')

@djity_view(perm='manage')
def inherit_style(request,js_target,context=None):
    project = context['project']
    if project.parent:
        project.css.set_all_values(project.parent.css.get_context())
        js_target.message(_("Style of the current project has been overwritten by the style of its parent \"%s\"" % project.parent.name),post=True)
        js_target.reload()
    else:
        js_target.message(_("The current project is root and cannot inherit its style"))

register('inherit_style')

