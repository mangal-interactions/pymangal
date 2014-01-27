.. _contributing:

How to upload data
==================

This page will walk you through the upload of a simple food web with three
species. The goal is to cover the basic mechanisms. To upload data, a good
knowledge of the data specification is important. ``JSON`` schemes are
imported when connecting to the database the first time ::

   >>> import pymangal as pm
   >>> api = pm.mangal(usr='myUserName', pwd='myPassword')
   >>> api.schemes.keys()

Sending data into the database is done though the ``Post`` method of the
``mangal`` class. The ``Post`` method requires two arguments: ``resource``
and ``data``. ``resource`` is the  type of object you are sending in the
database, and ``data`` is the object as a python ``dict``.::

   >>> my_taxa = {'name': 'Carcharodon carcharias', 'vernacular': 'Great white shark', 'eol': 213726, 'status': 'confirmed'}
   >>> great_white = api.Post('taxa', my_taxa)

The ``mangal`` API is configured so that, when data are received or modified,
it will *return* the database record created. It means that you can assign
the result of calling ``Post`` to an object, for easy re-use. For example,
we can now create a population belonging to this taxa: ::

   >>> my_population = {'taxa': great_white['id'], 'name': 'Amity island sharks'}
   >>> amity_island = api.Post('population', my_population)

.. note::
   In the ``rmangal`` package, it is possible to pass whole objects rather than just ``id`` to the function to patch and post. This is not the case with ``pymangal``.

Example: a linear food chain
----------------------------

In this exercice, we'll upload a linear food chain made of a top predator
(*Canis lupus*), a consumer (*Alces americanus*), and a primary producer
(*Abies balsamea*).

The first step is to create objects containing the taxa: ::

   >>> wolf = {'name': 'Canis lupus', 'vernacular': 'Gray wolf', 'status': 'confirmed'}
   >>> moose = {'name': 'Alces americanus', 'vernacular': 'American moose', 'status': 'confirmed'}
   >>> fir = {'name': 'Abies balsamea', 'vernacular': 'Balsam fir', 'status': 'confirmed'}

Now, we will take each of these objects, and send them into the database: ::

   >>> wolf = api.Post('taxa', wolf)
   >>> moose = api.Post('taxa', moose)
   >>> fir = api.Post('taxa', fir)

The next step is to create interactions between these taxa: ::

   >>> w_m = api.Post('interaction', {'taxa_from': wolf['id'], 'taxa_to': moose['id'], 'link_type': 'predation', 'obs_type': 'litterature'})
   >>> m_b = api.Post('interaction', {'taxa_from': moose['id'], 'taxa_to': fir['id'], 'link_type': 'herbivory', 'obs_type': 'litterature'})

That being done, we will now create a network with the different interactions: ::

   >>> net = api.Post('network', {'name': 'Isle Royale National Park', 'interactions': map(lambda x: x['id'], [w_m, m_b])})

The last step is to put this network into a dataset: ::

   >>> ds = api.Post('dataset', {'name': 'Test dataset', 'networks': [net['id']]})

And with these steps, we have (i) created taxa, (ii) established interactions
between them, (iii) put these interactions in a network, and (iv) created
a dataset.

Other notes
-----------

Conflicting names
~~~~~~~~~~~~~~~~~

The ``mangal`` API will check for the uniqueness of some properties before
writing the data. For example, no two taxa can have the same name, of
taxonomic identifiers. If this happens, the server will throw a ``500``
error, and the error message will tell you which field is not unique. You
can then use the filtering_ abilities to retrieve the pre-existing record.

Automatic validation
~~~~~~~~~~~~~~~~~~~~

So as to avoid sending "bad" data on the database, ``pymangal`` conducts an
automated validation of user-supplied data *before* doing anything. In case
the data are not properly formatted, a ``ValidationError`` will be thrown,
along with an explanation of (i) which field(s) failed to validate and (ii)
what acceptable values were.

Resource IDs and URIs
~~~~~~~~~~~~~~~~~~~~~

The ``pymangal`` module will, internaly, take care of replacing objects
identifiers by their proper URIs. If you want to make a reference to the
``taxa`` whose ``id`` is ``1``, the ``Post`` method will automatically convert
``1`` to ``api/v1/taxa/1/``, *i.e.* the format needed to upload.
