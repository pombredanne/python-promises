# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see
# <http://www.gnu.org/licenses/>.


"""
Unit-tests for python-promises multithreading support

:author: Christopher O'Brien  <obriencj@gmail.com>
:license: LGPL v.3
"""


from promises.multithread import ThreadExecutor, ProxyThreadExecutor
from .multiprocess import TestProcessExecutor


class TestThreadExecutor(TestProcessExecutor):
    """
    Create promises which will deliver in a separate thread.
    """

    def executor(self):
        return ThreadExecutor()


class TestProxyThreadExecutor(TestProcessExecutor):
    """
    Create transparent proxy promises which will deliver in a separate
    thread.
    """

    def executor(self):
        return ProxyThreadExecutor()


#
# The end.
