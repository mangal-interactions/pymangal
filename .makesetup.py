# -*- coding: utf-8 -*-
import os

with open('.version', 'r') as f:
    v = f.readline().rstrip()

SETUP = """
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
        name='pymangal',
        version='{0}',
        description='A client library for the mangal API',
        author='Timothée Poisot',
        author_email='tim@poisotlab.io',
        url='http://pymangal.readthedocs.org/en/latest/',
        download_url='https://github.com/mangal-wg/pymangal/tarball/{0}',
        packages=['pymangal'],
        keywords=['ecology','biology']
        )
""".format(v)

with open('setup.py', 'w') as s:
    s.write(SETUP)
