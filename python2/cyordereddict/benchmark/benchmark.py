import sys

import cyordereddict

from .magic_timeit import magic_timeit


SETUP_TEMPLATE = """
from {module} import OrderedDict
list_data = list(enumerate(range(1000)))
dict_data = dict(list_data)
ordereddict = OrderedDict(dict_data)
"""

BENCHMARKS = cyordereddict.OrderedDict([
    ('``__init__`` empty', 'OrderedDict()'),
    ('``__init__`` list', 'OrderedDict(list_data)'),
    ('``__init__`` dict', 'OrderedDict(dict_data)'),
    ('``__setitem__``', "ordereddict[0] = 0"),
    ('``__getitem__``', "ordereddict[0]"),
    ('``update``', "ordereddict.update(dict_data)"),
    ('``__iter__``', "list(ordereddict)"),
    ('``items``', "ordereddict.items()"),
    ('``__contains__``', "0 in ordereddict"),
])

if sys.version_info[0] >= 3:
    BENCHMARKS['``items``'] = 'list(%s)' % BENCHMARKS['``items``']


def _time_execution(module, code, repeat):
    setup = SETUP_TEMPLATE.format(module=module)
    result = magic_timeit(setup, code, repeat=repeat, force_ms=True)
    return result['timing']


def _calculate_benchmarks(repeat):
    all_results = []
    for bench_name, code in BENCHMARKS.items():
        stdlib_speed = _time_execution('collections', code, repeat)
        cy_speed = _time_execution('cyordereddict', code, repeat)
        ratio_str = '%.1f' % (stdlib_speed / cy_speed)
        all_results.append((bench_name, '``%s``' % code, ratio_str))
    return all_results


def benchmark(repeat=10):
    """Benchmark cyordereddict.OrderedDict against collections.OrderedDict
    """
    columns = ['Test', 'Code', 'Ratio (stdlib / cython)']
    res = _calculate_benchmarks(repeat)
    try:
        from tabulate import tabulate
        print(tabulate(res, columns, 'rst'))
    except ImportError:
        print(columns)
        print(res)
