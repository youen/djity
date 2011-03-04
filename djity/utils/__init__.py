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
    result = []
    for module in settings.DJITY_MODULES:
        djity_module = import_module(module).djity_module
        result.append(getattr(import_module('%s.models'%module),djity_module))

    return result
