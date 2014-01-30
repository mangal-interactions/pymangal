# -*- coding: utf-8 -*-
__version__ = '0.2.0'
__title__ = 'pymangal'
__author__ ='Timothée Poisot'
__license__ = 'BSD-2'

from api import mangal
from makeschema import makeschema

numVer = map(int, __version__.split('.'))
if numVer[0] == '0':
    unstableMess = "pymangal v."+__version__+" - this is an UNSTABLE release"
    if not numVer[2] == 0 :
        unstableMess += ", development version"
    print unstableMess
