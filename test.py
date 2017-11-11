from timeit import Timer
from pprint import pprint
from itertools import starmap, repeat, product, count
from collections import defaultdict


def a(ls, ns):
    return [(l, n) for l in ls for n in ns]


def b(ls, ns):
    d = defaultdict(set)
    # list(map(lambda i: d[i[0]].add(i[1]), product(ls, ns)))
    for k, v in product(ls, ns):
        d[k].add(v)
    return d


def runner(func, inputs):
    print(list(starmap(func, inputs)))


inputs = [
    [range(10), 'abcdefghij'],
    # list(range(100000000)),
]

t_a = Timer("runner(a, inputs)", globals=globals())
t_b = Timer("runner(b, inputs)", globals=globals())

# r_times = 5
# n_times = 10000
r_times = 1
n_times = 1

print('a : {:.10f}'.format(min(t_a.repeat(r_times, n_times))))
print('b : {:.10f}'.format(min(t_b.repeat(r_times, n_times))))
