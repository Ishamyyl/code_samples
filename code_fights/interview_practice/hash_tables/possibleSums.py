""" Given an array of integers nums and an integer k, determine whether there are two distinct indices i and j
in the array where nums[i] = nums[j] and the absolute difference between i and j is less than or equal to k.

my : 0.1013799411
tv : 0.1196780831
tv2: 0.1557239390
"""
from timeit import Timer
from pprint import pprint
from itertools import starmap


def myPossibleSums(coins, quantity):
    sums = {0}
    for coin, q in zip(coins, quantity):
        sums |= {i + choice for choice in range(coin, coin * q + 1, coin) for i in sums}
    return len(sums) - 1


def runner(func, inputs):
    pprint(list(starmap(func, inputs)))


inputs = [
    [[10, 50, 100], [1, 2, 1]],
    [[10, 50, 100, 500], [5, 3, 2, 2]],
    [[1], [5]],
    [[1, 1], [2, 3]],
    [[1, 2], [50000, 2]],
    [[1, 2, 3], [2, 3, 10000]],
    [[3, 1, 1], [111, 84, 104]],
    [[1, 1, 1, 1, 1], [9, 19, 18, 12, 19]],
]

t_my = Timer("runner(myPossibleSums, inputs)", globals=globals())
# t_tv = Timer("runner(tvContainsCloseNums, inputs)", globals=globals())
# t_tv2 = Timer("runner(tv2ContainsCloseNums, inputs)", globals=globals())

# r_times = 5
# n_times = 10000
r_times = 1
n_times = 1

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
# print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
# print('tv2: {:.10f}'.format(min(t_tv2.repeat(r_times, n_times))))
