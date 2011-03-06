import copy

from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.datastructures import SortedDict
from django.utils.translation import get_language

LANGUAGE_CODE = 0
LANGUAGE_NAME = 1


def get_real_fieldname(field, lang=None):
    if lang is None:
       lang = get_language()
    return str('%s_%s' % (field, lang))


def get_real_fieldname_in_each_language(field):
    return [get_real_fieldname(field, lang[LANGUAGE_CODE])
            for lang in settings.LANGUAGES]


def canonical_fieldname(db_field):
    """ all "description_en", "description_fr", etc. field names will return "description" """
    return getattr(db_field, 'original_fieldname', db_field.name) # original_fieldname is set by transmeta


def get_all_translatable_fields(model):
    """ returns all translatable fields in a model (including superclasses ones) """
    model_trans_fields = set(getattr(model._meta, 'translatable_fields', []))
    for parent in model._meta.parents:
        parent_trans_fields = getattr(parent._meta, 'translatable_fields', [])
        model_trans_fields.update(parent_trans_fields)
    return tuple(model_trans_fields)


def get_lang_version(instance,field):
 
    attname = lambda x: get_real_fieldname(field, x)
    def has_attr(lang):
        return getattr(instance, attname(lang),None)
    if  has_attr(get_language()):
        result = get_language()
    elif has_attr(get_language()[:2]):
        result = get_language()[:2]
    elif has_attr(instance.transmeta_default_language):
        result = instance.transmeta_default_language
    elif getattr(instance, attname(settings.LANGUAGE_CODE), None):
            result = settings.LANGUAGE_CODE
    else:
            result = getattr(settings, 'TRANSMETA_DEFAULT_LANGUAGE', 'en')
    return result


def default_value(field):
    '''
    When accessing to the name of the field itself, the value
    in the current language will be returned. Unless it's set,
    the value in the default language will be returned.
    '''

    attname = lambda lang: get_real_fieldname(field, lang)

    def has_attr(instance,lang):
        return  getattr(instance, attname(lang),None)




    def default_value_func(self):

        if  has_attr(self,get_language()):
            result = getattr(self, attname(get_language()))
        elif has_attr(self,get_language()[:2]):
            result = getattr(self, attname(get_language()[:2]))
        elif has_attr(self,self.transmeta_default_language):
            result = getattr(self, attname(self.transmeta_default_language))
        elif getattr(self, attname(settings.LANGUAGE_CODE), None):
            result = getattr(self, attname(settings.LANGUAGE_CODE))
        else:
            default_transmeta_attr = attname(
                getattr(settings, 'TRANSMETA_DEFAULT_LANGUAGE', 'en')
            )
            result = getattr(self, default_transmeta_attr, None)
        return result

    return default_value_func

def default_set_value(field):
    '''
    When settings to the name of the field itself, the value
    is set in the current language field. Unless it's set,
    the value is set in the default language field.
    '''
    def default_set_value_func(self,value):
        attname = lambda x: get_real_fieldname(field, x)
        
        if hasattr(self, attname(get_language())) :
            setattr(self, attname(get_language()),value)
        elif hasattr(self, attname(get_language()[:2])):
            setattr(self, attname(get_language()[:2]),value)
        elif hasattr(self, attname(self.transmeta_default_language)):
            setattr(self, attname(self.transmeta_default_language,value))
        elif hasattr(self, attname(settings.LANGUAGE_CODE)):
            setattr(self, attname(settings.LANGUAGE_CODE),value)
        else:
            default_transmeta_attr = attname(
                getattr(settings, 'TRANSMETA_DEFAULT_LANGUAGE', 'en')
            )
            setattr(self, default_transmeta_attr, value)
        

    return default_set_value_func

class TransMeta(models.base.ModelBase):
    '''
    Metaclass that allow a django field, to store a value for
    every language. The syntax to us it is next:

        class MyClass(models.Model):
            __metaclass__ transmeta.TransMeta

            my_field = models.CharField(max_length=20)
            my_i18n_field = models.CharField(max_length=30)

            class Meta:
                translate = ('my_i18n_field',)

    Then we'll be able to access a specific language by
    <field_name>_<language_code>. If just <field_name> is
    accessed, we'll get the value of the current language,
    or if null, the value in the default language.
    '''

    def __new__(cls, name, bases, attrs):
        attrs = SortedDict(attrs)
        # we inherits possible translatable_fields from superclasses
        inherits_translatable_fields = []
        abstract_model_bases = [base for base in bases if hasattr(base, '_meta')]
        for base in abstract_model_bases:
            if hasattr(base._meta, 'translatable_fields'):
                inherits_translatable_fields.extend(list(base._meta.translatable_fields))


        if 'Meta' in attrs and hasattr(attrs['Meta'], 'translate'):
            fields = attrs['Meta'].translate
            delattr(attrs['Meta'], 'translate')

            if hasattr(attrs['Meta'], 'ordering'):
                for field in  fields:
                    if field in attrs['Meta'].ordering :
                        ordering = list(attrs['Meta'].ordering)
                        index = ordering.index(field)
                        ordering[index] = field+'_'+ getattr(settings, 'TRANSMETA_DEFAULT_LANGUAGE', 'en')
                        attrs['Meta'].ordering = tuple(ordering)
                            

        
        else:
            new_class = super(TransMeta, cls).__new__(cls, name, bases, attrs)
            new_class._meta.translatable_fields = tuple(inherits_translatable_fields)
            return new_class

        if not isinstance(fields, tuple):
            raise ImproperlyConfigured("Meta's translate attribute must be a tuple")

        default_language = getattr(settings, 'TRANSMETA_DEFAULT_LANGUAGE', \
                                   settings.LANGUAGE_CODE)

        # no default_translateble_field for sub classes
        if inherits_translatable_fields == []:
            default_language_field = models.CharField(
                            max_length=5,
                            verbose_name='default language',
                            default= default_language)
            attrs['transmeta_default_language'] = default_language_field

        for field in fields:
            if not field in attrs or \
               not isinstance(attrs[field], models.fields.Field):
                    raise ImproperlyConfigured(
                        "There is no field %(field)s in model %(name)s, "\
                        "as specified in Meta's translate attribute" % \
                        dict(field=field, name=name))

            original_attr = attrs[field]

            for lang in settings.LANGUAGES:
                lang_code = lang[LANGUAGE_CODE]
                lang_attr = copy.copy(original_attr)
                
                original_attr.set_attributes_from_name(field) # Set the attributes now so we can use the column name later.
                if type(original_attr) == models.ForeignKey:
                    kwargs = {
                                'verbose_name': lang_attr.verbose_name,
                                'related_name': '%s_%s_set_%s' % (
									name.lower(),
									field,
									lang_code),

                                'limit_choices_to': lang_attr.rel.limit_choices_to,
                                'lookup_overrides': lang_attr.rel.lookup_overrides,
                                'parent_link': lang_attr.rel.parent_link,
                                }
                    lang_attr.__init__(lang_attr.rel.to, to_field=lang_attr.rel.field_name, **kwargs)
                
                lang_attr.original_fieldname = field
                lang_attr_name = get_real_fieldname(field, lang_code)
                if lang_code != default_language:
                    # only will be required for default language
                    if not lang_attr.null and lang_attr.default is NOT_PROVIDED:
                        lang_attr.null = True
                    if not lang_attr.blank:
                        lang_attr.blank = True
                if lang_attr.verbose_name:
                    lang_attr.verbose_name = u'%s %s' % (lang_attr.verbose_name, lang_code)
                attrs[lang_attr_name] = lang_attr
            del attrs[field]

            attrs[field] = property(default_value(field),default_set_value(field), doc=original_attr.column) # Set the column to __doc__ so we can access it later.
        new_class = super(TransMeta, cls).__new__(cls, name, bases, attrs)
        if hasattr(new_class, '_meta'):
            new_class._meta.translatable_fields = tuple(list(fields) + inherits_translatable_fields)
        return new_class
