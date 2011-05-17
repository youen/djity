# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import urllib
import logging

from django.http import HttpResponse,HttpResponseNotFound,HttpResponseForbidden,HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.conf import settings
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.http import urlquote
from django.contrib import messages
from django.core.urlresolvers import reverse

from django.template import RequestContext, loader
from djity.utils.context import DjityContext, JSTarget

from djity.project.models import Project
from djity.portlet.models import update_portlets_context
from djity.utils import djreverse

log = logging.getLogger('djity')

def djity_view(perm='view'):
    """
    This decorator is used by all views in files views.py and ajax.py
    that are declared as compatible with Djity.

    Its main task is to build a DjityContext instance depending on the current session,
     user and views parameters.

    It also checks that the permission required to access to the current view is satisfied
     by the current user in the current project.
    """

    def _dec(func):

        def _new_func(*args,**kwargs):
            # init context using request arguments
            request  = args[0]
            context = DjityContext(request)

            # Get project_name and module_name, standard parameters of djity
            # module views. Put them in the context.
            project_name = kwargs.get('project_name',None)
            context['project_name'] = project_name
            if project_name: del kwargs['project_name']

            module_name = kwargs.get('module_name',None)
            context['module_name'] = module_name
            if 'module_name' in kwargs: del kwargs['module_name']

            context['required_perm'] = perm

            # if the origin path is specified, clean it and set it
            if 'path' in kwargs:
                path = urllib.unquote(kwargs['path'])
                context['origin_path'] = path.split('?')[0]
                del kwargs['path']

            path = urlquote(request.get_full_path())
            context['path'] = path

            # Fetch project, or 404
            try:
                project = Project.objects.get(name=project_name)
            except Project.DoesNotExist:
                raise Http404

            # Check if a JS target is present
            js_target = kwargs.get('js_target',None)
            if js_target :
                context['js_target'] = JSTarget(js_target,request)
                kwargs['js_target'] = context['js_target']

            # set user, path and laguange values in context
            user = request.user
            context['user'] = request.user
            LANGUAGE_CODE = kwargs.get('LANGUAGE_CODE',None)
            if LANGUAGE_CODE :
                del kwargs['LANGUAGE_CODE']
                from django.utils.translation import activate
                activate(LANGUAGE_CODE)
            else:
                LANGUAGE_CODE = request.LANGUAGE_CODE
            context['LANGUAGE_CODE'] = LANGUAGE_CODE
            context['LANGUAGES'] = settings.LANGUAGES

            # the project itselt goes in the context
            context['project'] = project

            # the project also contributes to the context
            # actually permissions are resolved here
            project.update_context(context)

            # if the user is not allowed to use this view, redirect or ask for
            # authentication of return error
            if not perm in context['perm']:
                if not user.is_authenticated():
                    tup =  djreverse('login',context), REDIRECT_FIELD_NAME, path
                    messages.add_message(request, messages.INFO,unicode(_("You were redirected because you lacked a permission: "))+unicode(perm))
                    return HttpResponseRedirect('%s?%s=%s' % tup)
                else:
                    messages.add_message(request, messages.INFO,unicode(_("You were redirected because you lacked a permission: "))+unicode(perm))
                    return HttpResponseRedirect(djreverse('forbidden',context))

            # Add context of project and module level portlets
            update_portlets_context(context['project'],context)
            if 'module' in context:
                update_portlets_context(context['module'],context)

            #add info message from url in context
            if request.method == 'GET':
                if 'info_message' in request.GET:
                    context['info_message'] = request.GET['info_message']

            kwargs['context'] = context
             
            # if module was not found by projet.update_context() raise 404
            if module_name and not 'module' in context:
                context.message(_("This page does not exist on this project !"))
                context["module"] = {'label':_('Page not found')}
                templ = loader.get_template('djity/base.html')
                return HttpResponseNotFound(templ.render(context))

            if 'js_target' in context:
                func(*args,**kwargs)
                return context['js_target'].json()

            return func(*args,**kwargs)
        return _new_func

    return _dec
        
