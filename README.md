REPOSITORY DESCRIPTION
----------------------

This repository will contain small (or quite big) pieces of Python code I 
wrote to improve my Python programming experience. You can reuse it freely
under the terms of the GPL version 3 (see the LICENSE file of this repository,
or below for a short note).

REPOSITORY INDEX
----------------

- `testData`: a Python function decorator allowing to call a
[unittest](https://docs.python.org/library/unittest.html#module-unittest)
test fixture with multiple data under the control of a 
[unittest.TestCase.subTest()](https://docs.python.org/library/unittest.html#unittest.TestCase.subTest)
context manager. 

MAKING THE DOCUMENTATION
------------------------

The documentation of the utilities included in PythonUtils is provided as
Sphinx reStructuredText, which can be compiled into beatiful documentation
by [Sphinx](http://www.sphinx-doc.org).

To compile the documentation you have to install Sphinx, which can be done using
```
pip install -U sphinx
```
If you are using Unix, you will also need `make`, which is generally provided
by default.

Then `cd` into the `doc` subdirectory and run e.g.
```
make html
```
to generate HTML documentation. The documentation is output in `doc/_build` by default.

LICENSING INFORMATION
---------------------
These programs are free software: you can redistribute them and/or modify
them under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

These programs are distributed in the hope that they will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

