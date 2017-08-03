""" You are given an n x n 2D matrix that represents an image. Rotate the image by 90 degrees (clockwise).

Note: Try to solve this task in-place (with O(1) additional memory), since this is what you'll be asked to do during an interview

my : 0.0750591410
tv : 0.3928384482
tv2: 0.2982533208
"""
from timeit import Timer


def myRotateImage(a):
    return list(zip(*reversed(a)))


def tvRotateImage(a):
    a.reverse()
    for i in range(len(a)):
        for j in range(i):
            a[i][j], a[j][i] = a[j][i], a[i][j]
    return a


def tv2RotateImage(a):
    return [[x[i] for x in a][::-1] for i in range(len(a))]


def runner(func, inputs):
    list(map(func, inputs))


inputs = [
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]],
    [[1]],
    [[10, 9, 6, 3, 7],
     [6, 10, 2, 9, 7],
     [7, 6, 3, 8, 2],
     [8, 9, 7, 9, 9],
     [6, 8, 6, 8, 2]],
    [[40, 12, 15, 37, 33, 11, 45, 13, 25, 3],
     [37, 35, 15, 43, 23, 12, 22, 29, 46, 43],
     [44, 19, 15, 12, 30, 2, 45, 7, 47, 6],
     [48, 4, 40, 10, 16, 22, 18, 36, 27, 48],
     [45, 17, 36, 28, 47, 46, 8, 4, 17, 3],
     [14, 9, 33, 1, 6, 31, 7, 38, 25, 17],
     [31, 9, 17, 11, 29, 42, 38, 10, 48, 6],
     [12, 13, 42, 3, 47, 24, 28, 22, 3, 47],
     [38, 23, 26, 3, 23, 27, 14, 40, 15, 22],
     [8, 46, 20, 21, 35, 4, 36, 18, 32, 3]],
    [[33, 35, 8, 24, 19, 1, 3, 1, 4, 5],
     [25, 27, 40, 25, 17, 35, 20, 3, 19, 3],
     [9, 1, 9, 30, 9, 25, 32, 12, 15, 22],
     [30, 47, 25, 10, 18, 1, 19, 17, 43, 17],
     [40, 46, 42, 34, 18, 48, 29, 40, 31, 39],
     [37, 42, 37, 19, 45, 1, 4, 46, 48, 13],
     [8, 26, 31, 46, 44, 24, 34, 29, 12, 25],
     [45, 48, 36, 12, 33, 12, 4, 45, 22, 37],
     [33, 15, 34, 25, 34, 8, 50, 48, 30, 28],
     [18, 19, 22, 29, 15, 43, 38, 30, 8, 47]],
]

t_my = Timer("runner(myRotateImage, inputs)", globals=globals())
t_tv = Timer("runner(tvRotateImage, inputs)", globals=globals())
t2_tv = Timer("runner(tv2RotateImage, inputs)", globals=globals())

r_times = 5
n_times = 10000

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t2_tv.repeat(r_times, n_times))))
