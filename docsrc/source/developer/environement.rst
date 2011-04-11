Development environement
=========================



Virtualenv
----------
A virtual environment is mostly useful for a developer's working environment and more generally to put djity in a box separated from the rest of your system. You are free to skip this part if it is not relevant to your needs.
See `<http://virtualenv.openplans.org/>`_, and `<http://www.doughellmann.com/projects/virtualenvwrapper/>`_ to learn more about the tools we recommend.
You will need to have virtualenvwrapper installed, you can find installation instructions here: `<http://www.doughellmann.com/docs/virtualenvwrapper/install.html#basic-installation>`_.

Install Virtualenv
++++++++++++++++++

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

Install dependences
+++++++++++++++++++


Embed Dependences
-----------------

Djity embeded JS projects :

 * `JQuery <jquery.com>`_
 * `JQuery UI <jqueryui.com>`_
 * `ElRTE <http://elrte.org/>`_

System dependences
------------------
You have to install :

 * `Django <www.djangoproject.com/>`_
 * `Dajax <www.dajaxproject.com/>`_

Repository
----------

Djity use github as sources repository. Get the code source with::

	$ git clone git@github.com:djity/djity.git
	$ cd djity
	$ ./setup.py develop

You will be able to work on source code without repeating the installation.


Setup of a new project
----------------------

Now that djity and all its required packages are installed you can create a new development project::

	$ djity-admin.py create_project /path/to/my/project



