# Copyright 2012 Maru Newby <mnewby@thesprawl.net>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import unittest2 as unittest

from nosecurtain import (
    FilteredTraceback,
    TracebackFilter,
    )


class TestTracebackFilter(unittest.TestCase):

    def setUp(self):
        self.tb_filter = TracebackFilter()

    def test_collect_tracebacks(self):
        tb1 = mock.Mock()
        tb2 = mock.Mock()
        tb1.tb_next = tb2
        tb2.tb_next = None
        expected = [tb1, tb2]
        actual = self.tb_filter._collect_tracebacks(tb1)
        self.assertEqual(actual, expected)

    def test_filter_tracebacks_removes_last_traceback(self):
        tb1 = mock.Mock()
        tb2 = mock.Mock()
        tb1.tb_next = tb2
        tb2.tb_next = None
        tb1.tb_frame.f_code.co_filename = 'foo'
        tb2.tb_frame.f_code.co_filename = 'mox.py'
        expected = [tb1]
        actual = self.tb_filter(tb1)
        self.assertEqual(actual, expected)

    def test_filter_tracebacks_saves_prefixing_traceback(self):
        tb1 = mock.Mock()
        tb2 = mock.Mock()
        tb1.tb_next = tb2
        tb2.tb_next = None
        tb1.tb_frame.f_code.co_filename = 'mox.py'
        tb2.tb_frame.f_code.co_filename = 'foo.py'
        expected = [tb1, tb2]
        actual = self.tb_filter(tb1)
        self.assertEqual(actual, expected)

    def is_filtered_traceback(self, filename):
        tb = mock.Mock()
        tb.tb_frame.f_code.co_filename = filename
        return self.tb_filter._is_filtered_traceback(tb)

    def test_is_filtered_traceback_returns_true(self):
        self.assertTrue(self.is_filtered_traceback('mox.py'))

    def test_is_filtered_traceback_returns_false(self):
        self.assertFalse(self.is_filtered_traceback('foo'))


class TestFilteredTraceback(unittest.TestCase):

    def test_filter_traceback(self):
        tb1 = mock.Mock()
        tb2 = mock.Mock()
        tb1.tb_next = tb2
        tb2.tb_next = None
        tb1.tb_frame.f_code.co_filename = 'foo'
        tb2.tb_frame.f_code.co_filename = 'mox.py'
        ftb1 = FilteredTraceback(tb1)
        for attr in ['lasti', 'lineno', 'frame']:
            attr_name = 'tb_%s' % attr
            self.assertEqual(getattr(tb1, attr_name, None),
                             getattr(ftb1, attr_name, None))
        self.assertIsNone(ftb1.tb_next)
