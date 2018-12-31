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

class TestData:
    def __applyEnv(self):
        try:
            self.__prop = os.environ['TESTDATA_PROP']
        except(KeyError):
            pass
        if 'TESTDATA_SORT' in os.environ:
            self.__sort = True

    def __checkProp(self):
        if self.__prop == 'all':
            self.__prop = len(self.__data)
        elif (type(self.__prop) is str) and self.__prop.endswith('%'):
            self.__prop = ceil(float(self.__prop[:-1])/100*len(self.__data))
        else:
            self.__prop = int(self.__prop)
        if self.__prop <= 0:
            self.__prop = None

    def __init__(self, data, before=None, after=None, prop=1, sort=False, addIndexes=[]):
        self.__data = data
        if (len(self.__data) == 0):
            self.__caller = None
        elif (len(self.__data) == 1):
            self.__caller = self.__directCaller
        else:
            self.__caller = self.__subTestCaller

        self.__before = before
        self.__after = after
        self.__prop = prop
        self.__sort = sort
        self.__addIndexes = addIndexes

        self.__applyEnv()

        self.__checkProp()

    def __call__(self, fun):
        def testDataFun(testSelf):
            if self.__before is not None:
                self.__before(testSelf)
            self.__foreach(testSelf, fun)
            if self.__after is not None:
                self.__after(testSelf)
        return testDataFun

    def __foreach(self, testSelf, fun):
        if self.__caller is None:
            fun(testSelf)
        else:
            for msg, datum in self.__generator():
                self.__caller(testSelf, fun, msg, datum)

    def __generator(self):
        indexes = [i for i in range(len(self.__data)) if not i in self.__addIndexes]
        if self.__prop is not None:
            indexes = sample(indexes, min(len(indexes), self.__prop))
        indexes += self.__addIndexes
        if self.__sort:
            indexes.sort()

        if isinstance(self.__data, list):
            return [(None, self.__data[i]) for i in indexes]
        elif isinstance(self.__data, dict):
            dataItems = list(self.__data.items())
            return [dataItems[i] for i in indexes]

        raise ValueError('Test data must be a list or a dictionnary')

    def __directCaller(self, testSelf, fun, msg, datum):
        if isinstance(datum, dict):
            fun(testSelf, **datum)
        elif isinstance(datum, list) or isinstance(datum, tuple):
            fun(testSelf, *datum)
        else:
            fun(testSelf, datum)

    def __subTestCaller(self, testSelf, fun, msg, datum):
        if isinstance(datum, dict):
            with testSelf.subTest(msg=msg, **datum):
                fun(testSelf, **datum)
        elif isinstance(datum, list) or isinstance(datum, tuple):
            if msg is None:
                kwargs = {'arg' + str(a + 1) : v for a, v in enumerate(datum)}
            else:
                kwargs = {}
            with testSelf.subTest(msg=msg, **kwargs):
                fun(testSelf, *datum)
        else:
            with testSelf.subTest(msg=msg, arg=datum):
                fun(testSelf, datum)
