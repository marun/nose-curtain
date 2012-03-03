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

import os

from nose import plugins


__all__ = ['UnitFailureFormatter']


class FilteredTraceback(object):

    _ignored_filenames = [os.path.join('unittest2', 'case.py'),
                         'unittest.py']

    def __init__(self, tb):
        self._tb = tb
        self.tb_lasti = self._tb.tb_lasti
        self.tb_lineno = self._tb.tb_lineno
        self.tb_frame = self._tb.tb_frame

    def _is_unittest_frame(self, tb_frame):
        frame_filename = tb_frame.f_code.co_filename
        print frame_filename
        for filename in self._ignored_filenames:
            if frame_filename.endswith(frame_filename):
                return True
        return False

    @property
    def tb_next(self):
        tb_next = self._tb.tb_next
        if not tb_next:
            return
        # Ignore only the last unittest-related traceback
        if not tb_next.tb_next and self._is_unittest_frame(tb_next.tb_frame):
            return
        return FilteredTraceback(tb_next)


class UnitFailureFormatter(plugins.Plugin):

    def formatFailure(self, test, err):
        ec, ev, tb = err
        if tb:
            tb = FilteredTraceback(tb)
        return ec, ev, tb
