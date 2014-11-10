cyordereddict: Cython implementation of Python's collections.OrderedDict
========================================================================

A drop-in replacement for the standard library's ``OrderedDict`` that is
significantly faster.

To install::

	pip install cyordereddict

To use::

	try:
		from cyordereddict import OrderedDict
	except ImportError:
		from collections import OrderedDict
