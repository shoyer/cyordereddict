import cyordereddict

from .magic_timeit import magic_timeit


MODULES = ['cyordereddict', 'collections']

SETUP_TEMPLATE = """
from {module} import OrderedDict
list_data = list(enumerate(range(1000)))
dict_data = dict(list_data)
ordereddict = OrderedDict(dict_data)
"""

BENCHMARKS = [
    ('``__init__`` empty', 'OrderedDict()'),
    ('``__init__`` list', 'OrderedDict(list_data)'),
    ('``__init__`` dict', 'OrderedDict(dict_data)'),
    ('``__setitem__``', "ordereddict[-1] = False"),
    ('``__getitem__``', "ordereddict[100]"),
    ('``update``', "ordereddict.update(dict_data)"),
    ('``__iter__``', "list(ordereddict)"),
    ('``__contains__``', "100 in ordereddict"),
]


def _setup_ns(module):
    ns = globals().copy()
    setup = SETUP_TEMPLATE.format(module=module)
    exec setup in ns
    return ns


def _time_execution(module, code, repeat):
    ns = _setup_ns(module)
    result = magic_timeit(ns, code, repeat=repeat, force_ms=True)
    return result['timing']


def _calculate_benchmarks(repeat):
    all_results = []
    for bench_name, code in BENCHMARKS:
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
