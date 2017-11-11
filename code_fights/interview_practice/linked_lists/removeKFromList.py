""" Given a singly linked list of integers l and an integer k, remove all elements from list l that have a value equal to k.

Note: Try to solve this task in O(n) time using O(1) additional space, where n is the number of elements in the list, since this is what you'll be asked to do during an interview.

my : 0.4633369804
tv : 0.0707765322
tv2: 0.1025782161
"""
from timeit import Timer
from itertools import starmap


class ListNode(object):

    def __init__(self, x, n=None):
        self.value = x
        self.next = n

    def __str__(self):
        return "{}>{}".format(self.value, str(self.next))

    __repr__ = __str__


def myRemoveKFromList(l, k):
    pass
    # if l.next is None:
    #     return None
    # if l.value == k:
    #     return myRemoveKFromList(l.next, k)
    # return myRemoveKFromList(l, k)


def runner(func, inputs):
    print(list(starmap(func, inputs)))


inputs = [
    (ListNode(3, ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))), 3),
    # (ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(6, ListNode(7))))))), 10),
    # (ListNode(1000, ListNode(1000)), 1000),
    # (ListNode(None), -1000),
    # (ListNode(123, ListNode(456, ListNode(789, ListNode(0)))), 0),
]

t_my = Timer("runner(myRemoveKFromList, inputs)", globals=globals())
# t_tv = Timer("runner(tvFirstDuplicate, inputs)", globals=globals())
# t2_tv = Timer("runner(tv2FirstDuplicate, inputs)", globals=globals())

r_times = 1
n_times = 1

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
# print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
# print('tv2: {:.10f}'.format(min(t2_tv.repeat(r_times, n_times))))
