from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from dajax.core import Dajax
from djity.core.project.decorators import check_perm_and_update_context
from djity.utils.security import sanitize
from dajaxice.core import dajaxice_functions
register = lambda name:dajaxice_functions.register_function('djity.core.portlet.ajax',name)

from .models import TextPortlet

@check_perm_and_update_context(perm='edit')
def save_text_portlet(request,div_id,html,context=None):
    project = context['project']
    result =  Dajax()
    project_type = ContentType.objects.get_for_model(project.__class__)
    tp = TextPortlet.objects.get(container_id=project.id,container_type=project_type,div_id=div_id)
    html = sanitize(html)
    if tp.content != html :
        tp.content = html
        tp.save()
        msg = unicode(_('Change in portlet saved'))
        result.script('message("%s")'%msg)
    return result.json()

register('save_text_portlet')
