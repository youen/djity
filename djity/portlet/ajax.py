from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from dajax.core import Dajax
from djity.utils.decorators import djity_view
from djity.utils.security import sanitize
from dajaxice.core import dajaxice_functions
register = lambda name:dajaxice_functions.register_function('djity.portlet.ajax',name)

from .models import TextPortlet

@djity_view(perm='edit')
def save_text_portlet(request,js_target,div_id,html,context=None):
    
    tp = TextPortlet.objects.get(id=div_id)

    html = sanitize(html)
    if tp.content != html :
        tp.content = html
        tp.save()
        js_target.message(_('Change in portlet saved'))

register('save_text_portlet')
