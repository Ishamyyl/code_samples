#!/usr/bin/env python3
from timeit import Timer
import cProfile
from functools import partial
from operator import mod, pow
from itertools import repeat

def pow_p(a, b):
    return a ** 3

def pow_pp(a):
    return a ** 3
    
def mod_p(a, b):
    return a % b
    
def mod_pp(a):
    return a % 2

f = partial(pow_p, b=3)
g = partial(mod_p, b=2)

def t1():
    #lf = f
    #lg = g
    lf = pow_pp
    lg = mod_pp
    return [x ** 3 for x in range(1,281) if x % 2]

def t2():
    #lf = f
    #lg = g
    #lf = pow_pp
    #lg = mod_pp
    lf = getattr(3, '__rpow__')
    lg = getattr(2, '__rmod__')
    return list(map(lambda x: x ** 3, filter(lambda x: x % 2, range(1,281))))
    #return list(map(lf, filter(lg, range(1,281))))
    #return list(map(pow, *zip(filter(mod, *zip(range(1,281), repeat(2))), repeat(3))))

t_t1 = Timer("t1()", globals=globals())
t_t2 = Timer("t2()", globals=globals())

r_times = 5
n_times = 10000

print('t1 : {:.10f}'.format(min(t_t1.repeat(r_times, n_times))))
print('t2 : {:.10f}'.format(min(t_t2.repeat(r_times, n_times))))

cProfile.run("t1()")
cProfile.run("t2()")