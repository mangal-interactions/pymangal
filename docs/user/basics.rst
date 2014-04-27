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
latest version from the *GitHub* repository, using *e.g.*: ::

   wget https://github.com/mangal-wg/pymangal/archive/master.zip
   unzip master.zip
   cp pymangal-master/pymangal .
   rm -r pymangal-master

Then from within the ``pymangal`` folder, ::

   make requirements
   make test
   make install

Alternatively, ``make all`` will download the requirements, run the tests,
and install the module. Note that by default, the ``makefile`` calls
``python2`` and ``pip2``. If your versions of ptyhon 2 and pip are called,
*e.g.*, ``python27`` and ``pip``, you need to pass them as variable names when
calling make: ::

   make all pip=pip python=python27


Creating a mangal object
~~~~~~~~~~~~~~~~~~~~~~~~

Almost all of the actions you will do using ``pymangal`` will be done by
calling various methods of the ``mangal`` class. The usual first step of
any script is to import the module. ::
   
   >>> import pymangal as pm
   >>> api = pm.mangal()

Calling ``dir(api)`` will give you an overview of the methods and attributes.

APIs conforming to the ``mangal`` specification can expose either all
resources, or a subset of them. To see which are available, ::
   
   >>> api.resources

For each value in the previously returned list, there is an element of ::

   >>> api.schemes

This dictionary contains the ``json`` scheme for all resources exposed by
the API. This will both give you information about the data format, and be
used internally to ensure that the data you upload or patch in the remote
database are correctly formatted.

Getting a list of resources
---------------------------

``mangal`` objects have a ``List()`` method that will give a list of entries
for a type of resource. For example, one can list datasets with: ::

   >>> api.List('dataset')

The returned object is a ``dict`` with keys ``meta`` and ``objects``. ``meta``
is important because it allows paging through the resources, as we will
see below. The actual content you want to work with is within ``objects``;
``objects`` is an array of ``dict``.

Paging and offset
~~~~~~~~~~~~~~~~~

To preserve bandwidth (yours and ours), ``pymangal`` will only return the
first 10 records. The ``meta`` dictionary will give you the ``total_count``
(total number of objects) available. If you want to retrieve *all* of these
objects in a single request, you can use the ``page='all'`` argument to the
``List()`` method. ::

   >>> api.List('taxa', page='all')

If you want more that 10 records, you can pass the number of records to
``page``: ::

   >>> api.List('network', page=20)

An additional important attribute of ``meta`` is the ``offset``. It will
tell you how many objects were discarded before returning your results. For
example, the following code ::

   >>> t_1_to_4 = api.List('taxa', page=4, offset=0)
   >>> t_5_to_8 = api.List('taxa', page=4, offset=4)

is (roughly, you still would have to recompose the object) equivalent to ::

   >>> t_1_to_8 = api.List('taxa', page=8)

Filtering
~~~~~~~~~

There is a special page on filtering_. When filtering, it is recommended to
use ``page='all'``, as it will ensure that all matched results are returned.

Getting a particular resource
-----------------------------

Getting a particular resource required that you know its type, and its unique
identifier. For example, getting the ``taxa`` with ``id`` equal to 8 si ::

   >>> taxa_8 = api.Get('taxa', 8)

The object is returned *as is*, *i.e.* as a python ``Dict``. If there is
no object with the given ``id``, or no matching ``type``, then the call to
``Get`` will fail.

Creating and modifying resources
--------------------------------

There is a page dedicated to contributing_. Users with data that they want
to add to the *mangal* database are invited to read this page, which gives
informations about (1) how to register online and (2) how to prepare data
for upload.
