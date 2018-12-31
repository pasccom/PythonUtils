.. Copyright 2018 Pascal COMBES <pascom@orange.fr>
   
   Python test utils documentation file,
   written by Pascal COMBES on Thu Mar 22 23:04:04 2018.
   
   PythonUtils is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   PythonUtils is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with PythonUtils. If not, see <http://www.gnu.org/licenses/>

Test utils
==========

.. decorator:: TestData(data[, before=None, after=None, prop=1, sort=False, addIndexes=[]])

   This decorator is intended to be used on :mod:`unittest` fixtures.
   
   It runs the test fixture for each given datum in a :meth:`unittest.TestCase.subTest` context manager.
   Before running all the subtests in the fixture, it runs the function *before*, if not `None` and
   after running the fixture, it runs the function *after*, if not `None`.
   
   *data* can be:
   
   * A :class:`list`: the test fixture will be called on each item of the list without message
   * A :class:`dict`: the test fixture will be called on each value in the dictionnary with the corresponing key as message
       
   The :class:`list` or :class:`dict` items can be:
   
   * A :class:`tuple` or a :class:`list`: Each item corresponds to an argument of the test fixture function in sequential order
   * A :class:`dict`: Each element corresponds to an argument of the test fixture function depending on key.
       
   *prop* allows to subsample the test. It can be:

   * `'all'`: The test feature is run for all the data set
   * A percentage as a string (e.g. `'50%'` ): The test feature is run at least for this percentage of the data set
   * An integer (e.g. `2`): The test feature is run on this number of data elements

   This parameter can be overriden for all tests by the environment variable `TESTDATA_PROP` (using the same values).

   *sort* forces the sub tests to be executed in the order of the list (by default they are unsorted).
   Sorting sub tests can be forced by the environment variable `TESTDATA_SORT` (whatever its value).

   *addIndexes* is a :class:`list` of sub test indexes (beginning at `0`), which must always be run.

   Examples::
      
      @testData([
          {'a': -1, 'a2': 1},
          {'a': 0,  'a2': 0},
          {'a': 1,  'a2': 1},
      ])
      def testSquare(self, a, a2):
          self.assertEqual(a**2, a2)
    
      @testData({
          'negative': [-1, -1],
          'zero'    : [0,  0 ],
          'positive': [1,  1 ],
      ])
      def testCube(self, a, a3):
          self.assertEqual(a**3, a3)
