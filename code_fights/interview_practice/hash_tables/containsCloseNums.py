""" Given an array of integers nums and an integer k, determine whether there are two distinct indices i and j
in the array where nums[i] = nums[j] and the absolute difference between i and j is less than or equal to k.

my : 0.1013799411
tv : 0.1196780831
tv2: 0.1557239390
"""
from timeit import Timer
from itertools import starmap


def myContainsCloseNums(nums, k):
    mapping = {}
    for i, v in enumerate(nums):
        if v in mapping:
            if abs(mapping[v] - i) <= k:
                return True
        mapping[v] = i
    return False


def tvContainsCloseNums(nums, k):
    """ The top 4 or 5 were essentially identical to My
    """
    bucket = {}
    for i, num in enumerate(nums):
        if i - k > 0:
            deleteID = nums[i - k - 1]
            del bucket[deleteID]
        newID = num
        if num in bucket:
            return True
        bucket[newID] = num
    return False


def tv2ContainsCloseNums(nums, k):
    """ Tried to look for other variations, found this randomly
    """
    m = {}
    for index, x in enumerate(nums):
        if index > k:
            m[nums[index - k - 1]] -= 1
        if m.get(x, None) in [None, 0]:
            m[x] = 1
        else:
            return True
    return False


def runner(func, inputs):
    list(starmap(func, inputs))


inputs = [
    [[0, 1, 2, 3, 5, 2], 3],
    [[0, 1, 2, 3, 5, 2], 2],
    [[], 0],
    [[99, 99], 2],
    [[2, 2], 3],
    [[1, 2], 2],
    [[1, 2, 1], 2],
    [[1, 0, 1, 1], 1],
    [[1, 2, 1], 0],
    [[1, 2, 1], 1],
    [[1], 1],
    [[-1, -1], 1],
]

t_my = Timer("runner(myContainsCloseNums, inputs)", globals=globals())
t_tv = Timer("runner(tvContainsCloseNums, inputs)", globals=globals())
t_tv2 = Timer("runner(tv2ContainsCloseNums, inputs)", globals=globals())

r_times = 5
n_times = 10000
# r_times = 1
# n_times = 1

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t_tv2.repeat(r_times, n_times))))
