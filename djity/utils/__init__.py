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


def granted_perms(role,status):
    """
    return the list of permissions granted to a user according to his `role` and the `status` of a module
    """
    perms = filter(lambda p:has_perm(p,role,status), settings.PERMISSIONS)
    perms_dict = {}
    for p in perms:
        perms_dict[p] = True
    return perms_dict

def has_perm(permission,role,status):
    """
    Using constants defined in settings, determine if a role
    grants a permission according to a module status.
    """
    # update permission according to the current status if appropriate
    perm = settings.STATUS_PERMISSIONS[status].get(permission,permission)
    return role >= settings.PERMISSION_MIN_ROLE[perm]

