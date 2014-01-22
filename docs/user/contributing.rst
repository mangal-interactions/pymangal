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


