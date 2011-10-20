***************
Getting started
***************

Djity's current version being mainly directed towards developpers this guide is not written yet.
To quickly install and test Djity you should have a look at the Development environment page in
the Developers guide.

----------------------
Production environment
----------------------

Create a virtual environment and activate it (optional) :: 

 virtualenv  env_prod
 source env_prod/bin/activate

Download and install from the requirement file ::

 pip install -r wget https://github.com/djity/djity/raw/master/stable-req.txt

Create a Django project with the Djity's admin tool. Don't use the development option ::

 $djity-admin.py create_project prod
 Enter Project Label (The label of the root project of this instance of Djity) ['Djity']: 
 Enter Admin Name (Your name) ['admin']: 
 Enter Admin Email (Your email address) ['admin@example.com']: 
 Enter Develop (Build and run a default development project server and activate debug options (logging, templates and debug toolbar)  - y/N) ['N']: 
 setup a bare project in prod

Move into the new project ::

 cd prod/

Copy statics files into the current project ::	

 ./manage.py collectstatics

Configure the database in the local_settings.py ::

 vi local_settings.py

Create tables ::

 ./manage.py syncdb

Create the portal ::

 ./manage.py create_portal

Test your new project ::

 ./manage.py runserver --insecure
