# -*- coding: utf-8 -*-
__version__ = '0.1.2'
__title__ = 'pymangal'
__author__ ='Timothée Poisot'
__license__ = 'BSD-2'

from api import mangal
from makeschema import makeschema

if __version__[0] == '0':
    print "pymangal v."+__version__+" - this is an UNSTABLE release"
