**********************************
Write your first Djity application
**********************************

This tutorial is a mimic of the `django tutorial <http://docs.djangoproject.com/en/dev/intro/tutorial01/>`_.
If you don't know it, you should read/try it first.

Create a project
================

Djity is a django project, so you don't create a project !

Create a module
===============

A Djity module is a Django application that contains a class extended the class `Module` provided by `djity.core.project.models`.
This class should have the same name of your application (no case sensitive).

Create a standard Django application
------------------------------------

Use standard command to create an application::

	$ python manage.py startapp polls

and edit polls/models.py.

.. sourcecode:: python

	from djity.core.project.models import Module
	from djity.utils.inherit import SuperManager
	from django.db import models

	class Quiz(Module):
		"""
		A set of poll associated with a project.
		"""
		#get the module manager
		objects = SuperManager()


	class Poll(models.Model):
		poll = models.ForeignKey(Quiz)
		question = models.CharField(max_length=200)
		pub_date = models.DateTimeField('date published')

	class Choice(models.Model):
		poll = models.ForeignKey(Poll)
		choice = models.CharField(max_length=200)
		votes = models.IntegerField()

The `Quiz` class is a proxy between Djity and your module.
Edit  `polls/__init__.py` and import `Quiz` as `djity_module` :


.. sourcecode:: python

	from polls.models import Quiz as djity_module

Now, Djity know how to connect your module.







	


