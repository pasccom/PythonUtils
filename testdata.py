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
    """ TestData(data[, beforeAll=None, beforeEach=None, afterEach=None, afterAll=None, prop=1, sort=False, addIndexes=[]])

        This class acts as a decorator which is intended to be used on :mod:`unittest` fixtures.

        It runs the test fixture for each given datum in a :meth:`unittest.TestCase.subTest` context manager.
        Before running all subtests in the fixture, it runs the function *beforeAll*, if not ``None`` and
        after running all subtests in the fixture, it runs the function *afterAll*, if not ``None``.
        Before running each subtest in the fixture, it runs the function *beforeEach*, if not ``None`` and
        after running each subtest in the fixture, it runs the function *afterEach*, if not ``None``.

        **Parameters:**

        *data* -- can be:

        * A :class:`list`: the test fixture will be called on each item of the list without message
        * A :class:`dict`: the test fixture will be called on each value in the dictionnary with the corresponing key as message

        The :class:`list` or :class:`dict` items can be:

        * A :class:`tuple` or a :class:`list`: Each item corresponds to an argument of the test fixture function in sequential order
        * A :class:`dict`: Each element corresponds to an argument of the test fixture function depending on key.

        *beforeAll* -- A function to be run before all subtests in the fixture

        *beforeEach* -- A function to be run before each subtest in the fixture

        *afterEach* -- A function to be run after each subtest in the fixture

        *afterAll* -- A function to be run after all subtests in the fixture

        *prop* -- Allows to subsample the test. It can be:

        * ``'all'``: The test feature is run for all the data set
        * A percentage as a string (e.g. ``'50%'`` ): The test feature is run at least for this percentage of the data set
        * An integer (e.g. ``2``): The test feature is run on this number of data elements

        This parameter can be overriden for all tests by the environment variable ``TESTDATA_PROP`` (using the same values).

        *sort* -- forces the sub tests to be executed in the order of the :class:`list` (by default they are unsorted).
        Sorting is unsupported for :class:`dict` data sets (which are essentially unordered).
        Sorting sub tests can be forced by the environment variable ``TESTDATA_SORT`` (whatever its value).

        *addIndexes* -- is a :class:`list` of sub test indexes (beginning at ``0``) if *data* is a :class:`list`
        or keys if *data* is a :class:`dict`, which must always be run.

        **Examples**::

            @TestData([
                {'a': -1, 'a2': 1},
                {'a': 0,  'a2': 0},
                {'a': 1,  'a2': 1},
            ])
            def testSquare(self, a, a2):
                self.assertEqual(a**2, a2)

            @TestData({
                'negative': [-1, -1],
                'zero'    : [0,  0 ],
                'positive': [1,  1 ],
            })
            def testCube(self, a, a3):
                self.assertEqual(a**3, a3)
    """

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

    def __init__(self, data, beforeAll=None, beforeEach=None, afterEach=None, afterAll=None, prop=1, sort=False, addIndexes=[]):
        self.__data = data
        if (len(self.__data) == 0):
            self.__caller = None
        elif (len(self.__data) == 1):
            self.__caller = self.__directCaller
        else:
            self.__caller = self.__subTestCaller

        self.__beforeAll = beforeAll
        self.__beforeEach = beforeEach
        self.__afterEach = afterEach
        self.__afterAll = afterAll
        self.__prop = prop
        self.__sort = sort
        self.__addIndexes = addIndexes

        self.__applyEnv()

        self.__checkProp()

    def __call__(self, fun):
        def testDataFun(testSelf):
            if self.__beforeAll is not None:
                self.__beforeAll(testSelf)
            self.__foreach(testSelf, fun)
            if self.__afterAll is not None:
                self.__afterAll(testSelf)
        return testDataFun

    def __foreach(self, testSelf, fun):
        if self.__caller is None:
            self.__beforeEach(testSelf)
            fun(testSelf)
            self.__afterEach(testSelf)
        else:
            for msg, datum in self.__generator():
                self.__beforeEach(testSelf)
                self.__caller(testSelf, fun, msg, datum)
                self.__afterEach(testSelf)

    def __generator(self):
        if isinstance(self.__data, list):
            addIndexes = self.__addIndexes
        elif isinstance(self.__data, dict):
            keys = list(self.__data.keys())
            addIndexes = [keys.index(k) for k in self.__addIndexes]

        indexes = [i for i in range(len(self.__data)) if not i in addIndexes]
        if self.__prop is not None:
            indexes = sample(indexes, min(len(indexes), self.__prop))
        indexes += addIndexes
        if self.__sort:
            indexes.sort()

        if isinstance(self.__data, list):
            return [(None, self.__data[i]) for i in indexes]
        elif isinstance(self.__data, dict):
            return [(keys[i], self.__data[keys[i]]) for i in indexes]

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
