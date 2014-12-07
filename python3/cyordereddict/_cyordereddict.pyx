# directly copied from Lib/collections/__init__.py for Python 3 master

# For backwards compatibility, continue to make the collections ABCs
# available through the collections module.

from collections import MutableMapping, ValuesView, KeysView, ItemsView
from operator import eq as _eq
import sys as _sys
from reprlib import recursive_repr as _recursive_repr

from cpython.dict cimport PyDict_Clear, PyDict_DelItem, PyDict_SetItem
from cpython.object cimport Py_EQ, Py_NE
from cpython.weakref cimport PyWeakref_NewProxy

################################################################################
### OrderedDict
################################################################################

class _OrderedDictKeysView(KeysView):

    def __reversed__(self):
        yield from reversed(self._mapping)

class _OrderedDictItemsView(ItemsView):

    def __reversed__(self):
        for key in reversed(self._mapping):
            yield (key, self._mapping[key])

class _OrderedDictValuesView(ValuesView):

    def __reversed__(self):
        for key in reversed(self._mapping):
            yield self._mapping[key]

cdef class _Link(object):
    cdef public object prev, next, key
    cdef object __weakref__

@_recursive_repr()
def _repr__(self):
    if not self:
        return '%s()' % (self.__class__.__name__,)
    return '%s(%r)' % (self.__class__.__name__, list(self.items()))

cdef class OrderedDict(dict):
    'Dictionary that remembers insertion order'
    # An inherited dict maps keys to values.
    # The inherited dict provides __getitem__, __len__, __contains__, and get.
    # The remaining methods are order-aware.
    # Big-O running times for all methods are the same as regular dictionaries.

    # The internal self.__map dict maps keys to links in a doubly linked list.
    # The circular doubly linked list starts and ends with a sentinel element.
    # The sentinel element never gets deleted (this simplifies the algorithm).
    # The sentinel is in self.__hardroot with a weakref proxy in self.__root.
    # The prev links are weakref proxies (to prevent circular references).
    # Individual links are kept alive by the hard reference in self.__map.
    # Those hard references disappear when a key is deleted from an OrderedDict.

    cdef _Link __hardroot
    cdef object __root
    cdef dict __map

    def __init__(self, *args, **kwds):
        '''Initialize an ordered dictionary.  The signature is the same as
        regular dictionaries, but keyword arguments are not recommended because
        their insertion order is arbitrary.
        '''
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        if self.__root is None:
            self.__hardroot = _Link()
            self.__root = root = PyWeakref_NewProxy(self.__hardroot, None)
            root.prev = root.next = root
            self.__map = {}
        self.__update(*args, **kwds)

    def __setitem__(self, object key, object value):
        'od.__setitem__(i, y) <==> od[i]=y'
        # Setting a new item creates a new link at the end of the linked list,
        # and the inherited dictionary is updated with the new key/value pair.
        cdef _Link link
        if key not in self:
            self.__map[key] = link = _Link()
            root = self.__root
            last = root.prev
            link.prev, link.next, link.key = last, root, key
            last.next = link
            root.prev = PyWeakref_NewProxy(link, None)
        PyDict_SetItem(self, key, value)

    def __delitem__(self, object key):
        'od.__delitem__(y) <==> del od[y]'
        # Deleting an existing item uses self.__map to find the link which gets
        # removed by updating the links in the predecessor and successor nodes.
        PyDict_DelItem(self, key)
        link = self.__map.pop(key)
        link_prev = link.prev
        link_next = link.next
        link_prev.next = link_next
        link_next.prev = link_prev
        link.prev = None
        link.next = None

    def __iter__(self):
        'od.__iter__() <==> iter(od)'
        # Traverse the linked list in order.
        root = self.__root
        curr = root.next
        while curr is not root:
            yield curr.key
            curr = curr.next

    def __reversed__(self):
        'od.__reversed__() <==> reversed(od)'
        # Traverse the linked list in reverse order.
        root = self.__root
        curr = root.prev
        while curr is not root:
            yield curr.key
            curr = curr.prev

    def clear(self):
        'od.clear() -> None.  Remove all items from od.'
        root = self.__root
        root.prev = root.next = root
        self.__map.clear()
        PyDict_Clear(self)

    def popitem(self, bint last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.
        '''
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root.prev
            link_prev = link.prev
            link_prev.next = root
            root.prev = link_prev
        else:
            link = root.next
            link_next = link.next
            root.next = link_next
            link_next.prev = root
        key = link.key
        del self.__map[key]
        value = dict.pop(self, key)
        return key, value

    def move_to_end(self, object key, object last=True):
        '''Move an existing element to the end (or beginning if last==False).
        Raises KeyError if the element does not exist.
        When last=True, acts like a fast version of self[key]=self.pop(key).
        '''
        link = self.__map[key]
        link_prev = link.prev
        link_next = link.next
        link_prev.next = link_next
        link_next.prev = link_prev
        root = self.__root
        if last:
            last = root.prev
            link.prev = last
            link.next = root
            last.next = root.prev = link
        else:
            first = root.next
            link.prev = root
            link.next = first
            root.next = first.prev = link

    def __sizeof__(self):
        sizeof_ = _sys.getsizeof
        n = len(self) + 1                       # number of links including root
        # not relevant for extension types:
        # size = sizeof_(self.__dict__)            # instance dictionary
        size = sizeof_(self.__map) * 2          # internal dict and inherited dict
        size += sizeof_(self.__hardroot) * n     # link objects
        size += sizeof_(self.__root) * n         # proxy objects
        return size

    update = __update = MutableMapping.update

    def keys(self):
        "D.keys() -> a set-like object providing a view on D's keys"
        return _OrderedDictKeysView(self)

    def items(self):
        "D.items() -> a set-like object providing a view on D's items"
        return _OrderedDictItemsView(self)

    def values(self):
        "D.values() -> an object providing a view on D's values"
        return _OrderedDictValuesView(self)

    _ne__ = MutableMapping.__ne__

    __marker = object()

    def pop(self, object key, object default=__marker):
        '''od.pop(k[,d]) -> v, remove specified key and return the corresponding
        value.  If key is not found, d is returned if given, otherwise KeyError
        is raised.
        '''
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default is self.__marker:
            raise KeyError(key)
        return default

    def setdefault(self, object key, object default=None):
        'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
        if key in self:
            return self[key]
        self[key] = default
        return default

    def __repr__(self):
        'od.__repr__() <==> repr(od)'
        return _repr__(self)

    def __reduce__(self):
        'Return state information for pickling'
        # no need to pickle the instance dict because it doesn't exist here
        return self.__class__, (), None, None, iter(self.items())

    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, object iterable, object value=None):
        '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S.
        If not specified, the value defaults to None.
        '''
        self = cls()
        for key in iterable:
            self[key] = value
        return self

    def _eq__(self, object other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.
        '''
        if isinstance(other, OrderedDict):
            return dict.__eq__(self, other) and all(map(_eq, self, other))
        return dict.__eq__(self, other)

    def __richcmp__(self, other, int op):
        if op == Py_EQ:
            return self._eq__(other)
        if op == Py_NE:
            return self._ne__(other)
        return NotImplemented
