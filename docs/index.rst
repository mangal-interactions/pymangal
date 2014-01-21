.. pymangal documentation master file, created by
   sphinx-quickstart on Sat Jan 18 16:45:58 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pymangal
========

``pymangal`` is a library to interact with ``mangal`` API. It implements the basic methods (``Post``, ``Get``, ``List``, and ``Patch``).

::

   >>> import pymangal as pm
   >>> api = pm.mangal()
   >>> datasets = api.List('dataset', page='all')
   >>> print json.dumps(datasets['objects'], indent=3)
      [
      {
      "description": "Structure of local anemonefish-anemone networks across the Manado region of Sulawesi, Indonesia", 
      "id": "1", 
      "environment": [], 
      "papers": [
         "1"
      ], 
      "owner": "timpoisot", 
      "data": [
      "2"
      ], 
      "networks": [
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", 
      "14", "15", "16"
      ], 
      "name": "Indonesian anemonefish-anemone networks"
      }
      ]
   >>> print json.dumps(api.Get('network', 1), indent=3)
      {
      "description": null, 
      "interactions": [
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
      ], 
      "owner": "timpoisot", 
      "longitude": "124.819", 
      "environment": [], 
      "latitude": "1.585", 
      "date": null, 
      "id": "1", 
      "name": "Bahowo"
      }


The ``mangal`` class
--------------------

.. automodule:: pymangal

.. autoclass:: mangal
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

