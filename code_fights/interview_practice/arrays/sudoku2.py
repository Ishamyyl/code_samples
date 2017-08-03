""" Mine vs Top-Voted vs 2nd-Top-Voted
Sudoku is a number-placement puzzle. The objective is to fill a 9 × 9 grid with numbers in such a way that each column,
each row, and each of the nine 3 × 3 sub-grids that compose the grid all contain all of the numbers from 1 to 9 one time.

Implement an algorithm that will check whether the given grid of numbers represents a valid Sudoku puzzle according to the
layout rules described above. Note that the puzzle represented by grid does not have to be solvable.

my : 5.3253955709
tv : 0.0264164588
tv2: 6.2197226979

The `tv` algorithm has a much better Best Case, due to breaking early
"""
from itertools import chain
from timeit import Timer


def dup_in_list(lst):
    numbers_only = [n for n in lst if n != '.']
    return len(numbers_only) > len(set(numbers_only))


def dupeCheck(l):
    dup = set()
    return any(x in dup or dup.add(x) for x in l if x != '.')


def mySudoku2(grid):
    squares = (chain(grid[i][j:j + 3], grid[i + 1][j:j + 3], grid[i + 2][j:j + 3])
               for i in range(0, 9, 3) for j in range(0, 9, 3))
    cols = zip(*grid)
    return not any(map(dup_in_list, chain(grid, cols, squares)))


def check_unique(nums):
    s = set()
    for num in nums:
        if num == '.':
            continue
        if num in s:
            return False
        s.add(num)


def tvSudoku2(grid):
    return True
    for line in grid:
        if not check_unique(line):
            return False
    for i in range(9):
        if not check_unique([line[i] for line in grid]):
            return False
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not check_unique(grid[i][j:j + 3] + grid[i + 1][j:j + 3] + grid[i + 2][j:j + 3]):
                return False
    return True


def tv2Sudoku2(grid):
    h = []
    v = []
    sg = []
    for i in range(len(grid)):
        h.append('')
        for j in range(len(grid[0])):
            if i == 0:
                v.append('')
                sg.append('')
            if grid[i][j] == '.':
                pass
            else:
                if h[i].count(grid[i][j]) == 0:
                    h[i] += grid[i][j]
                else:
                    return False
                if v[j].count(grid[i][j]) == 0:
                    v[j] += grid[i][j]
                else:
                    return False
                if sg[(3 * (i // 3)) + (j // 3)].count(grid[i][j]) == 0:
                    sg[(3 * (i // 3)) + (j // 3)] += grid[i][j]
                else:
                    return False
    return True


def runner(func, inputs):
    list(map(func, inputs))


inputs = [
    [['.', '.', '.', '1', '4', '.', '.', '2', '.'],
     ['.', '.', '6', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '1', '.', '.', '.', '.', '.', '.'],
     ['.', '6', '7', '.', '.', '.', '.', '.', '9'],
     ['.', '.', '.', '.', '.', '.', '8', '1', '.'],
     ['.', '3', '.', '.', '.', '.', '.', '.', '6'],
     ['.', '.', '.', '.', '.', '7', '.', '.', '.'],
     ['.', '.', '.', '5', '.', '.', '.', '7', '.']],
    [[".", ".", ".", ".", "2", ".", ".", "9", "."],
     [".", ".", ".", ".", "6", ".", ".", ".", "."],
     ["7", "1", ".", ".", "7", "5", ".", ".", "."],
     [".", "7", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", "8", "3", ".", ".", "."],
     [".", ".", "8", ".", ".", "7", ".", "6", "."],
     [".", ".", ".", ".", ".", "2", ".", ".", "."],
     [".", "1", ".", "2", ".", ".", ".", ".", "."],
     [".", "2", ".", ".", "3", ".", ".", ".", "."]],
    [[".", ".", "4", ".", ".", ".", "6", "3", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     ["5", ".", ".", ".", ".", ".", ".", "9", "."],
     [".", ".", ".", "5", "6", ".", ".", ".", "."],
     ["4", ".", "3", ".", ".", ".", ".", ".", "1"],
     [".", ".", ".", "7", ".", ".", ".", ".", "."],
     [".", ".", ".", "5", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."]],
    [[".", ".", ".", ".", ".", ".", ".", ".", "2"],
     [".", ".", ".", ".", ".", ".", "6", ".", "."],
     [".", ".", "1", "4", ".", ".", "8", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", "3", ".", ".", ".", "."],
     ["5", ".", "8", "6", ".", ".", ".", ".", "."],
     [".", "9", ".", ".", ".", ".", "4", ".", "."],
     [".", ".", ".", ".", "5", ".", ".", ".", "."]],
    [[".", "9", ".", ".", "4", ".", ".", ".", "."],
     ["1", ".", ".", ".", ".", ".", "6", ".", "."],
     [".", ".", "3", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", "7", ".", ".", ".", ".", "."],
     ["3", ".", ".", ".", "5", ".", ".", ".", "."],
     [".", ".", "7", ".", ".", "4", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", "7", ".", ".", ".", "."]],
    [["7", ".", ".", ".", "4", ".", ".", ".", "."],
     [".", ".", ".", "8", "6", "5", ".", ".", "."],
     [".", "1", ".", "2", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", "9", ".", ".", "."],
     [".", ".", ".", ".", "5", ".", "5", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", "2", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."]],
    [[".", "4", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", "4", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", "1", ".", ".", "7", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", "3", ".", ".", ".", "6", "."],
     [".", ".", ".", ".", ".", "6", ".", "9", "."],
     [".", ".", ".", ".", "1", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", "2", ".", "."],
     [".", ".", ".", "8", ".", ".", ".", ".", "."]],
    [[".", ".", "5", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", "8", ".", ".", ".", "3", "."],
     [".", "5", ".", ".", "2", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "9"],
     [".", ".", ".", ".", ".", ".", "4", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "7"],
     [".", "1", ".", ".", ".", ".", ".", ".", "."],
     ["2", "4", ".", ".", ".", ".", "9", ".", "."]],
    [[".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", "9", ".", ".", ".", ".", ".", ".", "1"],
     ["8", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", "9", "9", "3", "5", "7", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", "4", "."],
     [".", ".", ".", "8", ".", ".", ".", ".", "."],
     [".", "1", ".", ".", ".", ".", "4", ".", "9"],
     [".", ".", ".", "5", ".", "4", ".", ".", "."]],
    [[".", ".", ".", "2", ".", ".", "6", ".", "."],
     [".", ".", ".", "1", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", "5", ".", "1", ".", ".", "8"],
     [".", "3", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", "9", ".", ".", ".", ".", "3"],
     ["4", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", "3", "8", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "4"]],
    [[".", ".", ".", ".", "8", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", "5", ".", "."],
     [".", ".", ".", ".", "4", ".", ".", "2", "."],
     [".", ".", ".", "3", ".", "9", ".", ".", "."],
     [".", ".", "1", "8", ".", ".", "9", ".", "."],
     [".", ".", ".", ".", ".", "5", "1", ".", "."],
     [".", ".", "3", ".", ".", "8", ".", ".", "."],
     [".", "1", "2", ".", "3", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", "7", ".", ".", "1"]],
    [[".", ".", ".", ".", ".", ".", "5", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     ["9", "3", ".", ".", "2", ".", "4", ".", "."],
     [".", ".", "7", ".", ".", ".", "3", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", "3", "4", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", "3", ".", ".", "."],
     [".", ".", ".", ".", ".", "5", "2", ".", "."]],
    [[".", ".", ".", ".", "4", ".", "9", ".", "."],
     [".", ".", "2", "1", ".", ".", "3", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "3"],
     [".", ".", ".", "2", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", "7", ".", ".", "."],
     [".", ".", ".", "6", "1", ".", ".", ".", "."],
     [".", ".", "9", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", "9", "."]],
    [[".", "8", "7", "6", "5", "4", "3", "2", "1"],
     ["2", ".", ".", ".", ".", ".", ".", ".", "."],
     ["3", ".", ".", ".", ".", ".", ".", ".", "."],
     ["4", ".", ".", ".", ".", ".", ".", ".", "."],
     ["5", ".", ".", ".", ".", ".", ".", ".", "."],
     ["6", ".", ".", ".", ".", ".", ".", ".", "."],
     ["7", ".", ".", ".", ".", ".", ".", ".", "."],
     ["8", ".", ".", ".", ".", ".", ".", ".", "."],
     ["9", ".", ".", ".", ".", ".", ".", ".", "."]],
    [[".", ".", ".", ".", ".", ".", ".", ".", "."],
     ["4", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", "6", ".", "."],
     [".", ".", ".", "3", "8", ".", ".", ".", "."],
     [".", "5", ".", ".", ".", "6", ".", ".", "1"],
     ["8", ".", ".", ".", ".", ".", ".", "6", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", "7", ".", "9", ".", ".", ".", "."],
     [".", ".", ".", "6", ".", ".", ".", ".", "."]],
    [[".", ".", ".", ".", ".", ".", ".", ".", "1"],
     [".", ".", ".", ".", ".", "6", ".", ".", "."],
     ["4", ".", ".", ".", ".", ".", "3", "8", "."],
     ["7", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", "5", "3", ".", ".", "."],
     [".", ".", ".", ".", "6", "8", ".", ".", "."],
     ["3", ".", ".", "9", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", "2", "1", "1", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."]],
    [[".", "8", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", "2", ".", ".", ".", "."],
     [".", "6", ".", ".", ".", ".", "1", ".", "4"],
     [".", ".", ".", "9", ".", ".", "7", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", "4", "."],
     [".", ".", "1", ".", ".", "8", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", "5", ".", "7", "."],
     [".", ".", "3", ".", ".", "5", "6", ".", "."]],
    [[".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", "2", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", "2", "7", "1", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", "2", ".", ".", ".", ".", ".", ".", "."],
     [".", "5", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", "9", ".", ".", ".", "8"],
     [".", ".", ".", ".", ".", "1", "6", ".", "."],
     [".", ".", ".", ".", "6", ".", ".", ".", "."]],
    [[".", ".", ".", "9", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", "3", ".", ".", ".", ".", ".", "1"],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     ["1", ".", ".", ".", ".", ".", "3", ".", "."],
     [".", ".", ".", ".", "2", ".", "6", ".", "."],
     [".", "9", ".", ".", ".", ".", ".", "7", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     ["8", ".", ".", "8", ".", ".", ".", ".", "."]],
    [[".", ".", ".", ".", ".", ".", "8", "3", "."],
     ["2", ".", ".", ".", ".", ".", ".", ".", "."],
     ["7", ".", ".", ".", ".", "7", ".", "9", "5"],
     [".", ".", ".", "1", ".", ".", ".", ".", "2"],
     [".", "8", ".", "9", ".", ".", ".", ".", "."],
     [".", ".", "5", "1", "9", ".", ".", ".", "."],
     ["5", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."],
     [".", ".", ".", ".", ".", ".", ".", ".", "."]]
]

t_my = Timer("runner(mySudoku2, inputs)", globals=globals())
t_tv = Timer("runner(tvSudoku2, inputs)", globals=globals())
t2_tv = Timer("runner(tv2Sudoku2, inputs)", globals=globals())

r_times = 5
n_times = 10000

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t2_tv.repeat(r_times, n_times))))
