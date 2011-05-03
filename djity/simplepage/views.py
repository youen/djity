from django.http import HttpResponse,HttpResponseNotFound,HttpResponseNotAllowed,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import *
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from djity.utils.decorators import djity_view
from djity.transmeta import get_lang_version



@djity_view()
def page(request,context=None):
    """
    Main view of the Wiki: page view
    """
    page = context['module']

    edit = 'edit' in context['perm']
    
    context['onload'] += 'lang_version = "%s";'% get_lang_version(page,'content')
#    if get_language()[:2] != get_lang_version(page,'content')[:2]:
#        if edit:
#            messages.add_message(request, messages.INFO,unicode(
#                _("The current page does not exist in %s, your are seeing the %s version. You can <a href='%s'>create draft now</a>!")%(get_language()[:2],get_lang_version(page,'content')[:2],'draft')))
#        else:
#            messages.add_message(request, messages.INFO,unicode(
#                _("The current page does not exist in %s, your are seeing the %s version.")%(get_language()[:2],get_lang_version(page,'content')[:2])))

    if page.content == "" and edit:
        page.content = _("The current page is empty, you can write some content.")

    context.update({'view':'page','page_content' : page.content,'advertising_context' : ['page_content']})
    return render_to_response('djity/simplepage/page.html',context)


