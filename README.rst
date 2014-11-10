========================================================================
cyordereddict: Cython implementation of Python's collections.OrderedDict
========================================================================

.. image:: https://travis-ci.org/shoyer/cyordereddict.svg?branch=master
    :target: https://travis-ci.org/shoyer/cyordereddict

A drop-in replacement for the standard library's ``OrderedDict`` that is
2-5x faster. Currently only for Python 2.7.

Benchmarks:
    ==================  =================================  =========================
    Test                Code                                 Ratio (stdlib / cython)
    ==================  =================================  =========================
    ``__init__`` empty  ``OrderedDict()``                                        1.7
    ``__init__`` list   ``OrderedDict(list_data)``                               3.3
    ``__init__`` dict   ``OrderedDict(dict_data)``                               3.1
    ``__setitem__``     ``ordereddict[-1] = False``                              2.9
    ``__getitem__``     ``ordereddict[100]``                                     2.4
    ``update``          ``ordereddict.update(dict_data)``                        2.7
    ``__iter__``        ``list(ordereddict)``                                    5.7
    ``items``           ``ordereddict.items()``                                  5.6
    ``__contains__``    ``100 in ordereddict``                                   2
    ==================  =================================  =========================

    Numbers larger than 1 mean cyorderedict is faster. To run yourself, use
    ``cyordereddict.benchmark()``.

Install:
    ``pip install cyordereddict``

Dependencies:
    cyorderedict is written with Cython, but requires no dependecies other than
    CPython and a C compiler.

Use:
    .. code-block:: python

        try:
            from cyordereddict import OrderedDict
        except ImportError:
            from collections import OrderedDict

License:
    MIT. cyordereddict is largely adapted from the Python standard library,
    which is available under the Python Software Foundation License.
