Localization
============

Interface localization
++++++++++++++++++++++

Djity use Django for the internalization/localisation `<http://docs.djangoproject.com/en/dev/topics/i18n/>`_.

Messages are generated in the locale directory of djity's package.

New language for python file and template can be add by ::
 
 django-admin.py makemessages -l zh -e py,html

and for Javascript files::

 django-admin.py makemessages -d djangojs -l zh 


update new messages::

 django-admin.py makemessages -a

