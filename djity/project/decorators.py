import urllib

from django.http import HttpResponse,HttpResponseNotFound,HttpResponseForbidden,HttpResponseRedirect, Http404
from django.conf import settings
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.http import urlquote
from django.contrib import messages
from django.core.urlresolvers import reverse

from django.template import RequestContext
from djity.utils.context import DjityContext

from djity.project.models import Project,Module,Role,Member
from djity.portlet.models import update_portlets_context

def check_perm_and_update_context(
        perm='view',
        login_url=None,
        redirect_field_name=REDIRECT_FIELD_NAME,
        redirect_url=None,
        redirect_args=None,
        ):
    """
    This decorator update the current context from path and user.
    """

    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL
    def _dec(func):

        def _new_func(*args,**kwargs):
            """
            Test for a project if module module_name is active 
            and save the project, instance of this module for this project in the context
            """
            
            request  = args[0]
            context = DjityContext(request)

            # Get project_name and module_name, standard parameters of djity
            # module views. Put them in the context.
            project_name = kwargs.get('project_name',None)
            context['project_name'] = project_name
            if project_name: del kwargs['project_name']

            module_name = kwargs.get('module_name',None)
            context['module_name'] = module_name
            if module_name: del kwargs['module_name']

            context['required_perm'] = perm

            # if the origin path is specified, clean it and set it
            if 'path' in kwargs:
                path = urllib.unquote(kwargs['path'])
                context['origin_path'] = path.split('?')[0]
                del kwargs['path']

            # Fetch project, or 404
            try:
                project = Project.objects.get(name=project_name)
        
            except Project.DoesNotExist:
                raise Http404

            user = request.user
            context['user'] = request.user
            path = urlquote(request.get_full_path())
            context['path'] = path
            LANGUAGE_CODE = kwargs.get('LANGUAGE_CODE',None)
            if LANGUAGE_CODE :
                del kwargs['LANGUAGE_CODE']
                from django.utils.translation import activate
                activate(LANGUAGE_CODE)
            else:
                LANGUAGE_CODE = request.LANGUAGE_CODE
            context['LANGUAGE_CODE'] = LANGUAGE_CODE
            context['LANGUAGES'] = settings.LANGUAGES

            context['project'] = project


            project.update_context(context)

            # if the user is not allowed to use this view, redirect or ask for
            # authentication of return error
            if perm not in context['perm']:
                if redirect_url:
                    redirect_kwargs = {'project_name':project_name}
                    if redirect_args:
                        for arg in redirect_args:
                            if arg == 'module_name':
                                redirect_kwargs[arg] = module_name
                            else:
                                redirect_kwargs[arg] = kwargs[arg]

                    r_url = reverse(redirect_url,kwargs=redirect_kwargs)
                    messages.add_message(request, messages.INFO,unicode(_("You were redirected because you lacked a permission: "))+unicode(perm))
                    return HttpResponseRedirect(r_url)
                if not user.is_authenticated():
                    tup =  login_url, redirect_field_name, path
                    return HttpResponseRedirect('%s?%s=%s' % tup)
                else:
                    return HttpResponseForbidden()
            context['project_public'] = project.is_public

            if module_name != None:
                try:
                    module = Module.objects.get(name=module_name,project=project).as_leaf_class()
                    
                    context['module'] = module
                    update_portlets_context(module,context)

                except Module.DoesNotExist:
                    raise Http404

            #add info or erro message from url in context
            if request.method == 'GET':
                if 'info_message' in request.GET:
                    context['info_message'] = request.GET['info_message']


            kwargs['context'] = context
            return func(*args,**kwargs)
        return _new_func

    return _dec
        
