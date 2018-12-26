# Copyright 2018 Pascal COMBES <pascom@orange.fr>
#
# This file is part of PythonUtils.
#
# PythonUtils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PythonUtils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonUtils. If not, see <http://www.gnu.org/licenses/>

import os
from math import ceil
from random import sample

def testData(data, before=None, after=None):
    def decorator(fun):
        def testDataFun(self):
            if before is not None:
                before(self)
            __foreachData(self, fun, data)
            if after is not None:
                after(self)
        return testDataFun
    return decorator 

def __foreachData(self, fun, data):
    if (len(data) == 0):
        fun(self)
        return
    elif (len(data) == 1):
        caller = __directCaller
    else:
        caller = __subTestCaller

    prop = 1
    try:
        prop = os.environ['TESTDATA_PROP']
        if prop == 'all':
            prop = len(data)
        elif prop.endswith('%'):
            prop = ceil(float(prop[:-1])/100*len(data))
        else:
            prop = int(prop)
        if prop <= 0:
            prop = None
    except(KeyError):
        pass

    for msg, datum in __generator(data, prop):
        caller(self, fun, msg, datum)
        
def __generator(data, prop=None):
    if prop is None:
        if isinstance(data, list):
            return zip([None]*len(data), data)
        elif isinstance(data, dict):
            return [(k, v) for k, v in data.items()]
    else:
        if isinstance(data, list):
            return zip([None]*prop, [data[i] for i in sorted(sample(range(len(data)), prop))])
        elif isinstance(data, dict):
            keys = list(data.keys())
            return [(keys[k], data[keys[k]]) for k in sorted(sample(range(len(keys)), prop))]

    raise ValueError('Test data must be a list or a dictionnary')
       
def __directCaller(self, fun, msg, datum):
    if isinstance(datum, dict):
        fun(self, **datum)
    elif isinstance(datum, list) or isinstance(datum, tuple):
        fun(self, *datum)
    else:
        fun(self, datum)
            
def __subTestCaller(self, fun, msg, datum):
    if isinstance(datum, dict):
        with self.subTest(msg=msg, **datum):
            fun(self, **datum)
    elif isinstance(datum, list) or isinstance(datum, tuple):
        if msg is None:
            kwargs = {'arg' + str(a + 1) : v for a, v in enumerate(datum)}
        else:
            kwargs = {}
        with self.subTest(msg=msg, **kwargs):
            fun(self, *datum)
    else:
        with self.subTest(msg=msg, arg=datum):
            fun(self, datum)
