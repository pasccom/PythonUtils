.. Python test utils documentation file,
   written by Pascal COMBES on Thu Mar 22 23:04:04 2018.
   
   Copyright 2018 Pascal COMBES <pascom@orange.fr>

Test utils
==========

.. decorator:: testData(data[, before=None, after=None])

   This decorator is intended to be used on :mod:`unittest` fixtures.
   
   It runs the test fixture for each given datum in a :meth:`unittest.TestCase.subTest` context manager.
   Before running the fixture, it runs the function *before*, if not `None` and
   after running the fixture, it runs the function *after*, if not `None`.
   
   *data* can be:
   
   * A :class:`list`: the test fixture will be called on each item of the list without message
   * A :class:`dict`: the test fixture will be called on each value in the dictionnary with the corresponing key as message
       
   The :class:`list` or :class:`dict` items can be:
   
   * A :class:`tuple` or a :class:`list`: Each item corresponds to an argument of the test fixture function in sequential order
   * A :class:`dict`: Each element corresponds to an argument of the test fixture function depending on key.
       
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
