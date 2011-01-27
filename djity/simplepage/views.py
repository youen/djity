from django.http import HttpResponse,HttpResponseNotFound,HttpResponseNotAllowed,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import *
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from djity.core.project.decorators import check_perm_and_update_context
from djity.services.transmeta.forms import LocalForm
from djity.services.transmeta import get_lang_version, is_draft, get_draft, set_as_draft


from .forms import SimplePageForm 

@check_perm_and_update_context()
def page(request,context=None):
    """
    Main view of the Wiki: page view
    """
    page = context['module']
    
    context['onload'] += 'lang_version = "%s";'% get_lang_version(page,'content')
    print  get_lang_version(page,'content')
    if get_language()[:2] != get_lang_version(page,'content')[:2]:
        if 'edit' in map(unicode,context['perm']):
            if is_draft(page,'content'):
                messages.add_message(request, messages.INFO,unicode(
                    _("The current page is a draft in %s, your are seeing the %s version. You can <a href='%s'>edit draft here</a>!")%(get_language()[:2],get_lang_version(page,'content')[:2],'draft')))
            else :
                messages.add_message(request, messages.INFO,unicode(
                    _("The current page does not exist in %s, your are seeing the %s version. You can <a href='%s'>create draft now</a>!")%(get_language()[:2],get_lang_version(page,'content')[:2],'draft')))
        else:
            messages.add_message(request, messages.INFO,unicode(
                _("The current page does not exist in %s, your are seeing the %s version.")%(get_language()[:2],get_lang_version(page,'content')[:2])))

    if page.content == "" and 'edit' in map(unicode,context['perm']):
        page.content = _("The current page is empty, you can write some content.")

    context.update({'view':'page','page_content' : page.content,'advertising_context' : ['page_content']})
    return render_to_response('core/simplepage/page.html',context)

@check_perm_and_update_context(perm='edit',redirect_url='simplepage-view',redirect_args=['module_name'])
def draft(request,context=None):
    """
    Edit a draft version
    """
    page = context['module']
    
    context['onload'] += 'lang_version = "%s";'% get_language()
    
    if not is_draft(page,'content'):
        if get_lang_version(page,'content') != get_language():
            set_as_draft(page,'content')
            messages.add_message(request, messages.INFO,
                    unicode('New draft for %s version created you can <a href="publish" title="publish this draft">publish it</a>'%get_language()))
            page.content =  _(u"<p>The current page is a draft in %s, your can edit it, but the %s version will be view while you don't publish this draft.</p>"%(
                    get_language()[:2],
                    get_lang_version(page,'content')[:2])
                ) + page.content
            page.save()
        else:
            messages.add_message(request, messages.INFO,
                    unicode('The %s version is not a draft')%get_language())
            return HttpResponseRedirect(reverse('simplepage-view', kwargs={'project_name':context['project_name'],'module_name':context['module_name']}))

    else :
        messages.add_message(request, messages.INFO,
                unicode('Your are editing the draft of the %s')%get_language())


    context.update({'view':'page','page_content' : get_draft(page,'content'),'advertising_context' : ['page_content']})
    return render_to_response('core/simplepage/page.html',context)


@check_perm_and_update_context(perm='edit',redirect_url='simplepage-view',redirect_args=['module_name'])
def publish(request,context=None):
    """
    publish a draft version
    """
    page = context['module']
    set_as_draft(page,'content',False)
    page.save()
    messages.add_message(request, messages.INFO,
                unicode('Draft published'))
    return HttpResponseRedirect(reverse('simplepage-view', kwargs={'project_name':context['project_name'],'module_name':context['module_name']}))


    
@check_perm_and_update_context(perm='edit',redirect_url='simplepage-view',redirect_args=['module_name'])
def edit(request,context=None):
    """
    Edit a simple page
    """
    page = context['module']

    from django.utils import translation

    if request.method == 'POST': # If the form has been submitted...
        form = LocalForm(SimplePageForm,request.POST , instance = page)
        try:
            form.save()
            messages.add_message(request, messages.INFO,unicode(_("The content of this page has been saved.")))
            return HttpResponseRedirect(reverse('simplepage-view', kwargs={'project_name':context['project_name'],'module_name':context['module_name']}))
        except:
            print form.errors.as_text()
    else:
        form = LocalForm(SimplePageForm,instance = page)

    context.update({'view':'edit','form' :form, 'advertising_context' : []})
    return render_to_response('core/simplepage/page_edit.html',context)

