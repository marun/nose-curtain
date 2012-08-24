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


__all__ = ['Curtain']


default_ignored_filenames = [
    'mox.py',
    'unittest.py',
    os.path.join('unittest', 'case.py'),
    os.path.join('unittest2', 'case.py'),
    ]


class TracebackFilter(object):

    def __init__(self, ignored_filenames=None):
        if not ignored_filenames:
            ignored_filenames = default_ignored_filenames
        self.ignored_filenames = ignored_filenames

    def __call__(self, tb):
        filtered_tracebacks = self._collect_tracebacks(tb)
        while filtered_tracebacks:
            # Only filter tracebacks from the end of the chain
            if self._is_filtered_traceback(filtered_tracebacks[-1]):
                filtered_tracebacks.pop()
            else:
                break
        return filtered_tracebacks

    def _collect_tracebacks(self, tb):
        last_tb = tb
        tracebacks = []
        while last_tb:
            tracebacks.append(last_tb)
            last_tb = last_tb.tb_next
        return tracebacks

    def _is_filtered_traceback(self, tb):
        frame_filename = tb.tb_frame.f_code.co_filename
        for filename in self.ignored_filenames:
            if frame_filename.endswith(filename):
                return True
        return False


class FilteredTraceback(object):

    def __init__(self, tb, filtered_tracebacks=None, ignored_filenames=None):
        self._tb = tb
        self.tb_lasti = self._tb.tb_lasti
        self.tb_lineno = self._tb.tb_lineno
        self.tb_frame = self._tb.tb_frame
        if not filtered_tracebacks:
            filtered_tracebacks = TracebackFilter(ignored_filenames)(tb)
        self._filtered_tracebacks = filtered_tracebacks

    @property
    def tb_next(self):
        tb_next = self._tb.tb_next
        if not tb_next or tb_next not in self._filtered_tracebacks:
            return
        return FilteredTraceback(tb_next, self._filtered_tracebacks)


class Curtain(plugins.Plugin):
    """Hide tracebacks of testing modules."""

    def _filter_tracebacks(self, test, err):
        ec, ev, tb = err
        if tb:
            tb = FilteredTraceback(tb,
                                   ignored_filenames=self.ignored_filenames)
        return ec, ev, tb

    def configure(self, options, conf):
        plugins.Plugin.configure(self, options, conf)
        self.conf = conf
        if options.curtain_filenames:
            ignored_filenames = options.curtain_filenames.split(',')
        else:
            ignored_filenames = default_ignored_filenames
        self.ignored_filenames = ignored_filenames

    def options(self, parser, env):
        plugins.Plugin.options(self, parser, env)
        parser.add_option("--curtain-filenames",
                          default=env.get("NOSE_CURTAIN_FILENAMES", ''),
                          dest="curtain_filenames",
                          help="Filter tracebacks for modules with the "
                               "given filenames. "
                               "[NOSE_CURTAIN_FILENAMES] or %s" %
                               default_ignored_filenames)

    def formatError(self, test, err):
        return self._filter_tracebacks(test, err)

    def formatFailure(self, test, err):
        return self._filter_tracebacks(test, err)
