from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from dajax.core import Dajax
from djity.core.project.decorators import check_perm_and_update_context
from djity.utils.security import sanitize
from djity.services.transmeta import is_draft
from dajaxice.core import dajaxice_functions
register = lambda name:dajaxice_functions.register_function('djity.core.simplepage.ajax',name)

@check_perm_and_update_context(perm='edit')
def save_simple_page(request,div_id,html,context=None):
    simple_page = context['module']
    result =  Dajax()
    html = sanitize(html)
    if simple_page.content != html :
        simple_page.content = html
        simple_page.save()
        if is_draft(simple_page,'content'):
            msg = unicode(_('Change in page saved, <a href=\\"publish\\" title=\\"Publish this draft\\">Publish it!</a>'))
        else:
            msg = unicode(_('Change in page saved'))
        result.script('message("%s")'%msg)
    return result.json()

register('save_simple_page')
