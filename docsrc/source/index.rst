.. Djity documentation master file, created by
   sphinx-quickstart on Fri Aug 13 13:58:11 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Djity's documentation!
=======================================

Djity Portal (referred to as Djity to make things shorter), is an open source Web development framework and Website engine built on top of `Django <http://www.djangoproject.com/>`_.
It's purpose is to help us (and maybe you !) build dynamic Web applications and publish them effortlessly on the Web.

Djity comes with a lot of things pre-processed for you: front-end site administration in AJAX, applications contained in tabulations, contextual portlets, skeletons for new applications and projects, shortcuts for asynchronous communications, Javascript libraries, a shared client and server side context dictionary, installation and documentation utilities, on page WYSIWYG HTML edition, easy internationalization, theming, etc.
A lot of the boilerplate stuff is taken care of. Applications can be exchanged and plugged on a server. That's nice, but of course there is a down side: all this comes with technical choices, constraints and an homogenized look and feel. Your choice !
We are focused on Web development using the latest standards (HTML5, CSS3, etc.), compatibility with older browsers is not a priority.

.. warning::
	Djity is still in an early development phase. If you are willing to look into it you should be prepared for gaps in functionalities and documentation, and for the occasional bug.

Features
--------

 * Projects tree (multiple projects on the same site, with different styles,
   users, etc.)
 * Users management (subscriptions, login, roles in projects, etc.)
 * 100% Ajax interface
 * Pluggable applications (instanciated in tabs of projects)
 * Easy generation of new Django instances and applications (using Skeleton)
 * Easy Ajax application developement (custom shortcuts and proxy objects based
   on Dajax and Dajaxice, integration of jquery and jquery-ui)
 * Enriched contextual dictionary both server and client side (with information about the current session,
   project, tab, users permissions, etc)
 * Online edition of the styles of the projects (using a custom themeroller
   inspired by jquery-ui)
 * Contextual portlets (per project and per instance of application in a
   project)
 * Easy internationalization of interface and user content (using i18n, django-localeurl and django-transmeta)
 * Rich WYSIWYG HTML edition wherever you want it (using eLRTE)

Incoming features
-----------------

 * Online administration of the portlets
 * Fully themable projects (not just some style parameters, but also the layouts)
 * Easy migration of data between versions (probably using South)
 * Integrated search engine (probably using Haystack)
 * User identification through OpenID
 * Recent advanced Web standards (PUSH, Websockets, etc)
 * Open data linking using standard ontologies (FOAF, SIOC, etc)

.. toctree::
	:maxdepth: 2
	
	tutorial/index.rst
	developer/index.rst
	api/modules.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

