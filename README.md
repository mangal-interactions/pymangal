# pymangal

`pymangal` is a `python` module to interact with the `mangal` API. The
documentation is here: <http://pymangal.readthedocs.org/en/latest/>

[![Build Status](https://travis-ci.org/mangal-wg/pymangal.png?branch=master)](https://travis-ci.org/mangal-wg/pymangal) [![Coverage Status](https://coveralls.io/repos/mangal-wg/pymangal/badge.png)](https://coveralls.io/r/mangal-wg/pymangal)

# Short tutorial

Contrary to the `rmangal` package, this module focuses on implementing a
minimal set of functions. it's a little less user-friendly, but easier to
maintain (and learn).

Dialogue with the API is handled by an instance of the `mangal` class. The
four most important functions are `List`, `Get`, `Post`, and `Patch` (to,
respectively, see a list of data, get a particular record, add new data,
and patch them).

```python
import pymangal
db = pymangal.mangal()
   
# Returns the first 20 datasets
db.List('dataset')

# Returns all datasets
db.List('dataset', autopage=True)

# Returns all interactions matching *parasitism
db.List('interaction', filters='link_type__endswith=parasitism', autopage=True)

# Get the first taxa
db.get('taxa', 1)
```
