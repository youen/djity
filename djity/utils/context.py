from django.template import RequestContext
from dajax.core.Dajax import Dajax
import json
from django.contrib import messages

class DjityJSONEncoder(json.JSONEncoder):
    def default(self,obj):
        return str(obj)

class JSONContext():
    def __init__(self,context):
        self.context = context
    def __repr__(self):
        return json.dumps(dict([(k,self.context[k]) for k in self.context._marked_as_json if (k != 'json_context' and k in self.context)]),cls=DjityJSONEncoder)

class DjityContext(RequestContext):

    def __init__(self,*args,**kwargs):
        RequestContext.__init__(self,*args,**kwargs)
        self._marked_as_json = set()
        #messages from django framwork
        self._marked_as_json.add('messages')
        self['messages'] = list(self['messages'])

        self['json_context'] = JSONContext(self)

    def __setitem__(self,key,value):
        RequestContext.__setitem__(self,key,value)
        self._marked_as_json.add(key)

    def __delitem__(self,key):
        RequestContext.__delitem__(key)
        del self._marked_as_json[key]

    def __iter__(self):
        for k in self._marked_as_json:
            yield (k,self[k])

    def mark_as_json(self,attr_name):
        self._marked_as_json.add(attr_name)

    def message(self,msg):
        self['messages'].append(unicode(msg))



class JSTarget(Dajax):
    """
    Interface to call javascript function on a target JS object from python
    """

    def __init__(self,target,request):
        Dajax.__init__(self)
        self._target = target
        self._request = request

    def message(self,message,post=False):
        """
        send a message to djity notification
        """
        if post:
            # use django to send message in response to the next request of
            # this session
            messages.add_message(self._request, messages.INFO, unicode(message))
        else:
            # Use ajax to display message on current page
            code = u"dj.message(%s);"%json.dumps(unicode(message))
            self.script(code)


    def reload(self):
        """
        reload the current page.
        """
        self.script("location.reload();")

    def __getattr__(self,name):
        """
        if `name` is a standard dajax function return that function or create and return  a stumb function.
        """
        try:
            return self.__dict__[name]
        except KeyError:
            def stumb(*args):
                jsargs = map(json.dumps,args)
                code = '%s.%s(%s)'%(self._target,name,','.join(jsargs))
                self.script(code)

            return stumb


