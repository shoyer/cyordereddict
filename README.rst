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

    To run these yourself, use ``cyordereddict.benchmark()``

Install:
    ``pip install cyordereddict``

Dependencies:
    CPython and a C compiler. Cython is only required for the dev version.

Use:
    .. code-block:: python

        from cyordereddict import OrderedDict

Cavaets:
    ``cyorderedddict.OrderedDict`` is an extension type (like the built-in
    ``dict``) instead of a Python class. This means that in a few pathological
    cases its behavior will defer from ``collections.OrderedDict``:

    * The ``inspect`` module does not work on ``cyorderedddict.OrderedDict``
      methods.
    * Extension types use slots intead of dictionaries, so you cannot add
      custom attributes without making a subclass (e.g.,
      ``OrderedDict.foo = 'bar'`` will fail).

    You can do anything else you might do with an OrderedDict, including making
    subclasses: everything else passes the ``collections.OrderedDict`` test
    suite.

License:
    MIT. cyordereddict is largely adapted from the Python standard library,
    which uses the Python Software Foundation License.
