from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.importlib import import_module

def djreverse(named_view,context,*args,**kwargs):
    if len(args) !=0:
        try:
            args.insert(0,context['project_name'])
        except KeyError:
            pass
        return reverse(named_view,args,kwargs)

    try:
        djkwargs = {'project_name':context['project_name']}
    except KeyError:
        djkwargs = {}

    djkwargs.update(kwargs)
    return reverse(named_view,kwargs=djkwargs)


def djity_modules():
    """
    Fetch classes defined by djity applications as container class. These classes
    are found in var djity_module of the__init__.py files. If this var is not defined
    it means that the application doesn't define a container class and cannot be displayed
    in separate tabs by djity.
    """
    result = []
    for module in settings.DJITY_APPS:
        try:
            djity_module = import_module(module).djity_module
            result.append(getattr(import_module('%s.models'%module),djity_module))
        except:
            pass

    return result


def perm_in_context(permission,context):
    """
    proxy to has_perm method, using djity's context to get parameters
    """
    return has_perm(permission,context['role'],context['module'].status)

def has_perm(permission,role,status):
    """
    Using constants defined in settings, determine if a role
    grants a permission according to a module status.
    """
    # update permission according to the current status if appropriate
    permission = settings.STATUS_PERMISSIONS[status].get(permission,permission)
    return role >= settings.PERMISSION_MIN_ROLE[permission]

