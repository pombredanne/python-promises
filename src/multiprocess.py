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

Multi-process Promises for Python

author: Christopher O'Brien  <obriencj@gmail.com>
license: LGPL v.3

"""


from abc import ABCMeta, abstractmethod
from multiprocessing.pool import Pool
from promises import ContainerPromise, ProxyPromise


class Promising(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def __promise__(self, work):
        """ must be overridden to provide a promise to do the
        specified work """
        return None

    def __init__(self, processes=None):
        self.__processes = processes
        self.__pool = None
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        # block until the queue is cleared up and all our promises
        # have been delivered

        if (exc_type is None):
            self.deliver()
        else:
            self.terminate()
        return (exc_type is None)

    def _spin_up(self):
        if not self.__pool:
            self.__pool = Pool(self.__processes)

    def promise(self, work):
        """ queue up a promise to be completed """

        self._spin_up()
        
        result = None
        promise = self.__promise__(lambda: result.get())
        result = self.__pool.apply_async(work, [], {})

        return promise

    def terminate(self):
        """ breaks all the remaining promises """
        self.__pool.terminate()
        self.__pool = None

    def deliver(self):
        """ blocks until all underlying promises have been delivered """
        self.__pool.close()
        self.__pool = None

    def is_delivered(self):
        return (self.__pool is None)


class ContainerPromising(Promising):
    def __promise__(self, work):
        return ContainerPromise(work)


class ProxyPromising(Promising):
    def __promise__(self, work):
        return ProxyPromise(work)


#
# The end.
