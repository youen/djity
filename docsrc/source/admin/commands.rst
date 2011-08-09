Project management commands
===========================

 * Prepare the databases. Useful in particular if you wish to update Djity for an existing project, or are modifying the models of an application used by the current project. (This is used automatically if you select the development mode of `djity-admin.py create_project`)::
 
    $ python manage.py syncdb
 
 * Create initial data for an empty project. (This is used automatically if you select the development mode of `djity-admin.py create_project`)::
 
    $ python manage.py create_portal
  
 * Run development server. (This is used automatically if you select the development mode of `djity-admin.py create_project`)::
 
    $ python manage.py runserver
  
 * Update search indexes. When the data of indexable contents from a project is modified, you should update all search indexes::
 
    $ python manage.py update_indexes --using=all
  
 * Install an application in the current project. You can use `djity-admin.py ls_apps` to list all installed apps in the system::
 
    $ python manage.py install_app <app>
