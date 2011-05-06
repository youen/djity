Documentation guide
===================

This guide gives instructions to contribute to the documentation of Djity.

However, Djity applications documentation is initialized in a very similar
manner. Therefore all instructions below could be applied also for good
documentation practices of Djity applications.


Using Sphinx
------------

`Sphinx <http://sphinx.pocoo.org/>`_ is a tool to create documentation
particularly appropriate for Python programs (being used for Python language
documentation itself).

All files related to the documentation can be found in the directory 'docsrc'
in Djity's root. You can edit files in the source sub-directory and use make to
produce the documentation ::

 make html

Results will be written in the 'build' sub-directory. Sometimes after important modifications
you may need to get back to a fresh start ::

 make clean

Writing tutorials
-----------------

In construction.

API
---

Python source API is automatically created when running 'make'. We don't have
particular guidelines yet for code documentation. However, every class and
function should have an associated docstring. We hope to put an effort for a
clean integration with Sphinx sooner or later.

