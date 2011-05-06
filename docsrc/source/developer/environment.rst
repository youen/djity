Development environment
=========================

Virtualenv
++++++++++

A virtual environment is mostly useful for a developer's working environment and more generally to put djity in a box separated from the rest of your system. You are free to skip this part if it is not relevant to your needs.
See `<http://virtualenv.openplans.org/>`_, and `<http://www.doughellmann.com/projects/virtualenvwrapper/>`_ to learn more about the tools we recommend.
You will need to have virtualenvwrapper installed, you can find installation instructions here: `<http://www.doughellmann.com/docs/virtualenvwrapper/install.html#basic-installation>`_.

Install Virtualenv
------------------

you can install virtualenv and virtualenvwrapper with pip::

	$ sudo pip install virtualenv
	$ sudo pip install virtualenvwrapper

update your bashrc::

	$ cat >> ~/.bashrc
	export WORKON_HOME=$HOME/.virtualenvs
	source /usr/local/bin/virtualenvwrapper.sh
	[ctrl+d]
	$ source ~/.bashrc

and create your virtualenv::

	$ mkdir ~/.virtualenvs
	$ mkvirtualenv djity

Afterwards, each time you want to work with djity you should type something like::

	$ workon djity

You can exit this environement with the deactivate command::

	$ deactivate

Dependencies
+++++++++++++++++++


Embedded dependencies
------------------

The source from some 3rd party programs are embedded for convenience. The list
below is for informational purpose, you don't need to do anything about it.

Djity embedded JS projects :

 * `JQuery <jquery.com>`_
 * `JQuery UI <jqueryui.com>`_
 * `ElRTE <http://elrte.org/>`_

Required dependencies
---------------------
You have to install :

 * `Django <http://www.djangoproject.com/>`_::
   
	$ pip install django

 * `Skeleton <http://pypi.python.org/pypi/skeleton>`_ (through our fork on
   github because of a small feature added)::

	$ git clone https://github.com/albanm/skeleton skeleton
	$ cd skeleton
	$ python setup.py install

 * `Dajax & Dajaxice <http://www.dajaxproject.com/>`_::
	
	$ pip install django-dajaxice
	$ pip install django-dajax

 * `django-localeurl <https://bitbucket.org/carljm/django-localeurl/>`_::
    
    $ pip install django-localeurl

 * `BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`_::

	$ pip install beautifulsoup

 * `Python Imaging Library <http://www.pythonware.com/products/pil/>`_::

   $ sudo apt-get install python-imaging
   
Optional dependences
--------------------

 * `Django Debug Toolbar <http://robhudson.github.com/django-debug-toolbar/>`_ (useful for developpers and required by option 'develop' of 'djity-admin.py create_project')::

   $ pip install django-debug-toolbar


Repository
++++++++++

Djity uses github as sources repository. Get the code source with::

	$ git clone git@github.com:djity/djity.git
	$ cd djity

You can now install Djity, to do so you can choose one of two different commands.

The command 'develop' is useful for contributors to Djity, it will create links so that you will be able to work on the source code
without repeating the installation::

	$ python setup.py develop

Non-contributors Web admins or application developpers should probably use the 'install' command::

	$ python setup.py install


Setup of a new project
++++++++++++++++++++++

Now that djity and all its required packages are installed you can create a new development project::

	$ djity-admin.py create_project /path/to/my/project


