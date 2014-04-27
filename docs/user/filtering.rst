.. _filtering:

Filtering of resources
======================

This document covers the different ways to filter resources using the
``List`` method.

General filtering syntax
------------------------

Filtering follows the general syntax::

   field__relation=target

``field`` is the name of one of the fields in the resource model (see
``mg.schemes[resource]['properties'].keys()``). ``relation`` is one of
the ten possible values given below. Finally, ``target`` is the value to
match. It is possible to join several filters, by joining them with ``&``.

Examples
~~~~~~~~

Let's start by loading the module::

   >>> import pymangal as pm
   >>> api = pm.mangal()

Getting all taxa whose name contains "alba"::

   >>> api.List('taxa', filters='name__contains=alba', page='all')

Getting the dataset containing network "101"::

   >>> api.List('dataset', filters='networks__in=101', page='all')

Getting all networks with "benthic" in their name, between latitudes "-5" and "5"::

   >>> api.list('network', filters='name__contains=bentic&latitude__range=-5,5', page='all')

Type of relationships
---------------------

==============  ========================================================
relation        description
==============  ========================================================
``startswith``  All fields starting by the target
``endswith``    All fields ending by the target
``exacts``      Exact matching
``contains``    Fields that contain the target
``range``       Fields with values in the range
``gt``          Field with values greater than the target
``lt``          Field with values smaller than the target
``gte``         Field with values greater (or equal to) than the target
``lte``         Field with values smaller (or equal to) than the target
``in``          Field with the target among their values
==============  ========================================================

Filtering through multiple resources
------------------------------------

It is possible to combine several resources when filtering. For example, if
one want to retrieve populations belonging to the taxa *Alces americanus*,
the syntax is ::

   taxa__name__exact=Alces%20americanus

Examples
~~~~~~~~

List of populations whose taxa is of the genus "Alces"::

   >>> api.List('population', filters='taxa__name__startswith=Alces', page='all')

List of interactions involving "Canis lupus" as a predator ::

   >>> api.List('interaction', filters='link_type__exact=predation&taxa_from__name__exact=Canis%20lupus', page='all')
