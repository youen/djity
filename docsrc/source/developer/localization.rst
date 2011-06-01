Language Localisation
=====================

Instructions below are for localisation/internationalization of Djity. However
Djity applications being organized in a very similar way, applications
developpers could be interested as well.

Interface localisation
++++++++++++++++++++++

Djity uses Django in a pretty standard way for internalization/localisation `<http://docs.djangoproject.com/en/dev/topics/i18n/>`_.

Messages are generated in the locale directory of djity's package. Commands
below should be used in the directory of Djity's main package (directory 'djity' in root).

A new language translation (chinese in the example below) for python file and template can be added by ::

 django-admin.py makemessages -l zh -e py,html

And for Javascript files ::

 django-admin.py makemessages -d djangojs -l zh 

You can update all messages for all languages by using ::

 django-admin.py makemessages -a
 django-admin.py makemessages -a -d djangojs

You should then edit files with extension '.po' in the locale directory. When
edition is over, you can compile messages that will be automaticaly applied
afterwards. ::

 django-admin.py compilemessages


User content localisation
+++++++++++++++++++++++++

Djity allows its users to define multi-language contents without any particular
administration action. No particular guide is written yet about this
functionality. You should switch languages (flags on the top-right corner), then edit pages contents and rename
tabs on a test project in order to get the idea.

