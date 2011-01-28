from django.forms.models import ModelFormMetaclass
from django.utils.translation import  get_language
from django.conf import settings
from django.forms import fields_for_model

def LocalForm(Form,*args,**kwargs):
    """
    Local form factory.
    keep the current language field and exclude other
    """


    class SubLocalForm(Form):
        def __init__(self):
            super(SubLocalForm,self).__init__(*args,**kwargs)
            if not hasattr(self.Meta,'exclude'):
                self.Meta.exclude = None
            if not hasattr(self.Meta,'fields'):
                self.Meta.fields = None
             
            self.fields = fields_for_model(
                    Form.Meta.model,
                    fields=self.Meta.fields,
                    exclude=self.Meta.exclude)
               
            print "fields", self.fields

        class Meta(Form.Meta):
            if hasattr(Form.Meta,'exclude'):
                exclude = Form.Meta.exclude[:]

            if hasattr(Form.Meta,'fields'):
                fields = Form.Meta.fields[:]

    model = Form.Meta.model
    # How to get translatable_fields from parents class ??
    trans_fields = model._meta.translatable_fields

    if hasattr(SubLocalForm.Meta,'exclude'):
        exclude_field = SubLocalForm.Meta.exclude
        for field in trans_fields:
            if field in exclude_field :
                SubLocalForm.Meta.exclude.remove(field)
                for lang in settings.LANGUAGES:
                    SubLocalForm.Meta.exclude.append('%s_%s'%(field,lang[0]))
            else:
                for lang in settings.LANGUAGES: 
                    if lang[0] != get_language()[:2] :
                        SubLocalForm.Meta.exclude.append('%s_%s'%(field,lang[0]))
    
    elif hasattr(SubLocalForm.Meta,'fields'):
        fields = SubLocalForm.Meta.fields
        for field in trans_fields:
            if field in fields:
                SubLocalForm.Meta.fields.remove(field)
                SubLocalForm.Meta.fields.append('%s_%s'%(field,get_language()[:2]))

            
    return SubLocalForm()


