import operator
import unittest

import cyordereddict


class TestOrderedDict(unittest.TestCase):
    def setUp(self):
        data = [('x', 0), ('y', 1), ('z', 2)]
        self.data = cyordereddict.OrderedDict(data)

    def test_rich_cmp(self):
        # verify rich comparison raises
        ops = [getattr(operator, o) for o in ['lt', 'le', 'gt', 'ge']]
        for op in ops:
            with self.assertRaises(TypeError):
                op(self.data, self.data)
            with self.assertRaises(TypeError):
                op(self.data, {})
            with self.assertRaises(TypeError):
                op({}, self.data)

    def test_delete_while_iterating(self):
        # regression test for GH9
        # should not raise
        od = cyordereddict.OrderedDict([('a', 1)])
        for (k, v) in od.items():
            del od[k]
