.. _basics:

pymangal 101
============

This document provides an overview of what the ``pymangal`` module can do,
and more importantly, how to do it. 

Overview of the module
----------------------

Installation
~~~~~~~~~~~~

At the moment, the simplest way to install ``pymangal`` is to download the
latest version from the *GitHub* repository, using *e.g.*:

   ::
   wget https://github.com/mangal-wg/pymangal/archive/master.zip
   unzip master.zip
   cp pymangal-master/pymangal .
   rm -r pymangal-master

Creating a mangal object
~~~~~~~~~~~~~~~~~~~~~~~~

Almost all of the actions you will do using ``pymangal`` will be done by
calling various methods of the ``mangal`` class. The usual first step of
any script is to import the module.
   
   ::
   >>> import pymangal as pm
   >>> api = pm.mangal()

Calling ``dir(api)`` will give you an overview of the methods and attributes.

APIs conforming to the ``mangal`` specification can expose either all
resources, or a subset of them. To see which are available,
   
   ::
   >>> api.resources

For each value in the previously returned list, there is an element of

   ::
   >>> api.schemes

This dictionary contains the ``json`` scheme for all resources exposed by
the API. This will both give you information about the data format, and be
used internally to ensure that the data you upload or patch in the remote
database are correctly formatted.

Getting a list of resources
---------------------------

Filtering
---------

There is a special page on filtering_.

Getting a particular resource
-----------------------------

Creating and modifying resources
--------------------------------

