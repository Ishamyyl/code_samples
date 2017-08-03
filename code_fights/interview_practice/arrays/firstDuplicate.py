""" Given an array a that contains only numbers in the range from 1 to a.length, find the first duplicate number
for which the second occurrence has the minimal index. In other words, if there are more than 1 duplicated numbers,
return the number for which the second occurrence has a smaller index than the second occurrence of the other number does.
If there are no such elements, return -1.

Note: Write a solution with O(n) time complexity and O(1) additional space complexity,
since this is what you would be asked to do during a real interview.

my : 0.4633369804
tv : 0.0707765322
tv2: 0.1025782161
"""
from collections import Counter
from timeit import Timer


def myFirstDuplicate(a):
    c = Counter()
    for i in a:
        if c[i] == 1:
            return i
        c[i] += 1
    return -1


def tvFirstDuplicate(a):
    mySet = set()
    for el in a:
        if el in mySet:
            return el
        mySet.add(el)
    return -1


def tv2FirstDuplicate(a):
    for i in a:
        a[abs(i) - 1] *= -1
        if a[abs(i) - 1] > 0:
            return abs(i)
    return -1


def runner(func, inputs):
    list(map(func, inputs))


inputs = [
    [2, 3, 3, 1, 5, 2],
    [2, 4, 3, 5, 1],
    [1],
    [2, 2],
    [2, 1],
    [2, 1, 3],
    [2, 3, 3],
    [3, 3, 3],
    [8, 4, 6, 2, 6, 4, 7, 9, 5, 8],
    [10, 6, 8, 4, 9, 1, 7, 2, 5, 3],
    [1, 1, 2, 2, 1],
]

t_my = Timer("runner(myFirstDuplicate, inputs)", globals=globals())
t_tv = Timer("runner(tvFirstDuplicate, inputs)", globals=globals())
t2_tv = Timer("runner(tv2FirstDuplicate, inputs)", globals=globals())

r_times = 5
n_times = 10000

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t2_tv.repeat(r_times, n_times))))
