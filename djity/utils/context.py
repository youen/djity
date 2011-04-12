from django.template import RequestContext
from dajax.core.Dajax import Dajax
import json

class DjityJSONEncoder(json.JSONEncoder):
    def default(self,obj):
        return str(obj)

class JSONContext():
    def __init__(self,context):
        self.context = context
    def __repr__(self):
         return json.dumps(dict([(k,self.context[k]) for k in self.context._marked_as_json if k != 'json_context']),cls=DjityJSONEncoder)

class DjityContext(RequestContext):

    def __init__(self,*args,**kwargs):
        RequestContext.__init__(self,*args,**kwargs)
        self._marked_as_json = set()
        #messages from django framwork
        self._marked_as_json.add('messages')
        self['django_messages'] = list(self['messages'])

        self['json_context'] = JSONContext(self)

    def __setitem__(self,key,value):
        RequestContext.__setitem__(self,key,value)
        self._marked_as_json.add(key)

    def mark_as_json(self,attr_name):
        self._marked_as_json.add(attr_name)



class JSTarget(Dajax):
    """
    Interface to call javascript function on a target JS object from python
    """

    def __init__(self,target):
        Dajax.__init__(self)
        self._target = target

    def __getattr__(self,name):
        """
        if `name` is a standard dajax function return that function or create and return  a stumb function.
        """
        print 'get attr', name
        try:
            return self.__dict__[name]
        except KeyError:
            def stumb(*args):
                jsargs = map(json.dumps,args)
                code = '%s.%s(%s)'%(self._target,name,','.join(jsargs))
                self.script(code)

            return stumb


