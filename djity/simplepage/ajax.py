from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _ 
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import get_language
from dajax.core import Dajax
from djity.utils.decorators import djity_view
from djity.utils.security import sanitize
from dajaxice.core import dajaxice_functions
register = lambda name:dajaxice_functions.register_function('djity.simplepage.ajax',name)


@djity_view(perm='edit')
def save_simple_page(request,js_target,html,context=None):
    simple_page = context['module']
    html = sanitize(html)
    if simple_page.content != html :
        simple_page.content = html
        simple_page.save()
        js_target.message(_('Change in page saved.'))

register('save_simple_page')
