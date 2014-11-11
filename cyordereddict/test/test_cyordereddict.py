import operator
import unittest

import cyordereddict


class TestOrderedDict(unittest.TestCase):
    def setUp(self):
        data = [('x', 0), ('y', 1), ('z', 2)]
        self.dicts = []
        try:
            import collections
            self.dicts.append(collections.OrderedDict(data))
        except AttributeError:
            # python 2.6
            pass
        self.dicts.append(cyordereddict.OrderedDict(data))

    def test_rich_cmp(self):
        # verify rich comparison still works as expected on Python 2
        ops = ['lt', 'le', 'gt', 'ge']
        for op in ops:
            for obj in self.dicts:
                f = getattr(operator, op)
                self.assertTrue(f(obj, {}) is not None)
                self.assertTrue(f({}, obj) is not None)
