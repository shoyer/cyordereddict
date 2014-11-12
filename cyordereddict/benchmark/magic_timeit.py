# Modified from Wes McKinley's vbench:
# https://github.com/pydata/vbench/blob/master/vbench/benchmark.py

# Modified from IPython project, http://ipython.org


def magic_timeit(setup, stmt, ncalls=None, repeat=3, force_ms=False):
    """Time execution of a Python statement or expression
    Usage:\\
      %timeit [-n<N> -r<R> [-t|-c]] statement
    Time execution of a Python statement or expression using the timeit
    module.
    Options:
    -n<N>: execute the given statement <N> times in a loop. If this value
    is not given, a fitting value is chosen.
    -r<R>: repeat the loop iteration <R> times and take the best result.
    Default: 3
    -t: use time.time to measure the time, which is the default on Unix.
    This function measures wall time.
    -c: use time.clock to measure the time, which is the default on
    Windows and measures wall time. On Unix, resource.getrusage is used
    instead and returns the CPU user time.
    -p<P>: use a precision of <P> digits to display the timing result.
    Default: 3
    Examples:
      In [1]: %timeit pass
      10000000 loops, best of 3: 53.3 ns per loop
      In [2]: u = None
      In [3]: %timeit u is None
      10000000 loops, best of 3: 184 ns per loop
      In [4]: %timeit -r 4 u == None
      1000000 loops, best of 4: 242 ns per loop
      In [5]: import time
      In [6]: %timeit -n1 time.sleep(2)
      1 loops, best of 3: 2 s per loop
    The times reported by %timeit will be slightly higher than those
    reported by the timeit.py script when variables are accessed. This is
    due to the fact that %timeit executes the statement in the namespace
    of the shell, compared with timeit.py, which uses a single setup
    statement to import function or create variables. Generally, the bias
    does not matter as long as results from timeit.py are not mixed with
    those from %timeit."""

    import timeit
    import math

    units = ["s", "ms", 'us', "ns"]
    scaling = [1, 1e3, 1e6, 1e9]

    timer = timeit.Timer(stmt, setup)

    if ncalls is None:
        # determine number so that 0.2 <= total time < 2.0
        number = 1
        for _ in range(1, 10):
            if timer.timeit(number) >= 0.1:
                break
            number *= 10
    else:
        number = ncalls

    best = min(timer.repeat(repeat, number)) / number

    if force_ms:
        order = 1
    else:
        if best > 0.0 and best < 1000.0:
            order = min(-int(math.floor(math.log10(best)) // 3), 3)
        elif best >= 1000.0:
            order = 0
        else:
            order = 3

    return {'loops': number,
            'repeat': repeat,
            'timing': best * scaling[order],
            'units': units[order]}
