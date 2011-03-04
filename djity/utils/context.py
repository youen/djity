from django.template import RequestContext
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



