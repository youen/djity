***************
Getting started
***************

Let's learn how to install a Djity instance.

Dependences
===========

Required
--------

* django > 1.2 :
  `http://www.djangoproject.com/download/`

* dajaxice :
  dajaxice 1.5 is broken you need to clone from our personal GIT
  `git@github.com:youen/django-dajaxice.git`

* dajax :
  http://dajaxproject.com/

Optional
--------

* django-extension


Install
=======

Get sources from djity's private git::

	$ git clone ssh://[username]@djity.net/home/alban/git/djityportal.git djity
	$ cd djity


Create your `settings_local.py`::

	$ cp settings_local.example settings_local.py

Edit it and configure your database and Create djity's tables with the `syncdb` command::

	$ ./manage syncdb

Create an admin user. Now you can create the portal::

	$ ./manage create_portal

Run the django server ::

	$ ./mange runserver


	





