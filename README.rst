=============
cyordereddict
=============

.. image:: https://travis-ci.org/shoyer/cyordereddict.svg?branch=master
    :target: https://travis-ci.org/shoyer/cyordereddict

.. image:: https://badge.fury.io/py/cyordereddict.svg
    :target: https://pypi.python.org/pypi/cyordereddict

The Python standard library's ``OrderedDict`` ported to Cython. A drop-in
replacement that is 2-6x faster.

Install:
    ``pip install cyordereddict``

Dependencies:
    CPython (2.6, 2.7, 3.3 or 3.4) and a C compiler. Cython is only required
    for the dev version.

Use:
    .. code-block:: python

        from cyordereddict import OrderedDict

Benchmarks:
    Python 2.7:

    ==================  =================================  =========================
    Test                Code                                 Ratio (stdlib / cython)
    ==================  =================================  =========================
    ``__init__`` empty  ``OrderedDict()``                                        1.8
    ``__init__`` list   ``OrderedDict(list_data)``                               4.8
    ``__init__`` dict   ``OrderedDict(dict_data)``                               4.6
    ``__setitem__``     ``ordereddict[0] = 0``                                   8.6
    ``__getitem__``     ``ordereddict[0]``                                       3
    ``update``          ``ordereddict.update(dict_data)``                        5.5
    ``__iter__``        ``list(ordereddict)``                                    5.6
    ``items``           ``ordereddict.items()``                                  5.9
    ``__contains__``    ``0 in ordereddict``                                     2.3
    ==================  =================================  =========================

    Python 3.4:

    ==================  =================================  =========================
    Test                Code                                 Ratio (stdlib / cython)
    ==================  =================================  =========================
    ``__init__`` empty  ``OrderedDict()``                                        1.5
    ``__init__`` list   ``OrderedDict(list_data)``                               3.9
    ``__init__`` dict   ``OrderedDict(dict_data)``                               4.2
    ``__setitem__``     ``ordereddict[0] = 0``                                   8.4
    ``__getitem__``     ``ordereddict[0]``                                       2.9
    ``update``          ``ordereddict.update(dict_data)``                        6.5
    ``__iter__``        ``list(ordereddict)``                                    2.3
    ``items``           ``list(ordereddict.items())``                            2.1
    ``__contains__``    ``0 in ordereddict``                                     2.3
    ==================  =================================  =========================
    To run these yourself, use ``cyordereddict.benchmark()``

Cavaets:
    ``cyorderedddict.OrderedDict`` is an extension type (similar to the
    built-in ``dict``) instead of a Python class. This is necessary for speed,
    but means that in a few pathological cases its behavior will differ from
    ``collections.OrderedDict``:

    * The ``inspect`` module does not work on ``cyorderedddict.OrderedDict``
      methods.
    * Extension types use slots instead of dictionaries, so you cannot add
      custom attributes without making a subclass (e.g.,
      ``OrderedDict.foo = 'bar'`` will fail).

    You can do anything else you might do with an OrderedDict, including
    subclassing: everything else passes the ``collections.OrderedDict`` test
    suite. We based the Cython code directly on the Python standard library,
    and thus use separate code bases for Python 2 and 3, specifically to
    reduce the potential for introducing new bugs.

License:
    MIT. Based on the Python standard library, which is under the Python
    Software Foundation License.
