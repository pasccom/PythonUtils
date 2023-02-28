# Copyright 2023 Pascal COMBES <pascom@orange.fr>
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

import unittest
import unittest.mock

from pathlib import Path

class MockOpen(unittest.mock.MagicMock):
    def __init__(self, *args, **kwArgs):
        super().__init__(*args, **kwArgs)
        if (len(args) > 0) and (type(args[0]).__name__ == 'function'):
            self.__dict__['resolver'] = args[0]

    def __call__(self, *args, **kwArgs):
        mockFile = super().__call__(*args, **kwArgs)
        if (type(mockFile).__name__ != 'MockOpen'):
            return mockFile
        mockFile.__enter__.return_value = mockFile

        if (len(args) > 0) and (type(args[0]) is MockPath):
            resolver = self.__dict__['resolver']
            path, contents = resolver(args[0])

            if ('mode' in kwArgs) and ('b' in kwArgs['mode']):
                mockFile.read.return_value = contents
            else:
                mockFile.read.return_value = contents.decode()
        return mockFile


class MockPath:
    def __init__(self, tree, path=None):
        self.__tree = tree
        self.__path = self.__cleanPath(path)

    def __str__(self):
        return self.__path

    def __repr__(self):
        return f'MockPath({self.__path})'

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.__path == str(other)
        elif type(other) is MockPath:
            return self.__path == other.__path
        else:
            return False

    def __call__(self, path=None):
        if self.__path is None:
            self.__path = self.__cleanPath(path)
            return self
        else:
            return MockPath(self.__tree, path)

    def __truediv__(self, path):
        return MockPath(self.__tree, self.__path + '/' + self.__cleanPath(path))

    @property
    def name(self):
        sep = self.__path.rfind('/')
        if (sep < 0):
            return self.__path
        else:
            return self.__path[(sep + 1):]

    @property
    def parents(self):
        path = self.__path
        sep = len(path)
        while True:
            sep = self.__path.rfind('/', 0, sep)
            if (sep <= 0):
                break
            yield MockPath(self.__tree, self.__path[0:sep])
            sep = sep - 1

    def exists(self):
        realPath, contents = self.__resolve()
        return contents is not None

    def is_file(self):
        realPath, contents = self.__resolve()
        return type(contents) is bytes

    def is_dir(self):
        realPath, contents = self.__resolve()
        return type(contents) is dict

    def resolve(self):
        self.__path, contents = self.__resolve()
        return self

    def iterdir(self):
        path, contents = self.__resolve()
        if type(contents) is dict:
            for p in contents:
                yield MockPath(self.__tree, path + '/' + p)

    def __resolve(self, path=None):
        if path is None:
            path = self.__path
        subTree = self.__tree
        for p in path.split('/'):
            if (len(p) == 0):
                continue
            if p not in subTree:
                return path, None
            elif type(subTree[p]) is dict: # folder
                subTree = subTree[p]
            elif type(subTree[p]) is str: # link
                return self.__resolve(self.__cleanPath(subTree[p]))
            else:
                return path, subTree[p]
        return path, subTree

    @staticmethod
    def __cleanPath(path):
        while (path is not None) and path.endswith('/'):
            path = path[:-1]
        return path

    @classmethod
    def mock_open(cls):
        return MockOpen(cls.__resolve)
