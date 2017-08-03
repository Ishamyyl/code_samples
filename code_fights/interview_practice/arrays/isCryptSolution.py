""" A cryptarithm is a mathematical puzzle for which the goal is to find the correspondence between letters and digits,
such that the given arithmetic equation consisting of letters holds true when the letters are converted to digits.

You have an array of strings `crypt`, the cryptarithm, and an an array containing the mapping of letters and digits, `solution`.
The array crypt will contain three non-empty strings that follow the structure: [word1, word2, word3],
which should be interpreted as the word1 + word2 = word3 cryptarithm.

If crypt, when it is decoded by replacing all of the letters in the cryptarithm with digits using the mapping in solution,
becomes a valid arithmetic equation containing no numbers with leading zeroes, the answer is true.
If it does not become a valid arithmetic solution, the answer is false.

my : 0.3940648157
tv : 0.3726561705
tv2: 0.4032622781
f  : 0.3497850925
"""
from timeit import Timer
from itertools import starmap


def myIsCryptSolution(crypt, solution):
    mapping = str.maketrans(dict(solution))
    a, b, c = (w.translate(mapping) for w in crypt)
    if '0' in list(zip(a, b, c))[0] and (len(a) > 1 and len(b) > 1 and len(c) > 1):
        return False
    return int(a) + int(b) == int(c)


def tvIsCryptSolution(crypt, solution):
    dic = {ord(c): d for c, d in solution}
    *v, = (w.translate(dic) for w in crypt)
    return not any(x != "0" and x.startswith("0") for x in v) and int(v[0]) + int(v[1]) == int(v[2])


def tv2IsCryptSolution(crypt_s, solution):
    for i in range(0, 3):
        for s in solution:
            crypt_s[i] = crypt_s[i].replace(s[0], s[1])
        if crypt_s[i] != '0' and crypt_s[i][0] == '0':
            return False
    if int(crypt_s[0]) + int(crypt_s[1]) != int(crypt_s[2]):
        return False
    return True


def fastest(crypt, solution):
    mapping = {ord(c): d for c, d in solution}
    *v, = (w.translate(mapping) for w in crypt)
    if not any(x != "0" and x.startswith("0") for x in v):
        return False
    return int(v[0]) + int(v[1]) == int(v[2])


def runner(func, inputs):
    list(starmap(func, inputs))


inputs = [
    (["SEND", "MORE", "MONEY"],
     [["O", "0"], ["M", "1"], ["Y", "2"], ["E", "5"],
      ["N", "6"], ["D", "7"], ["R", "8"], ["S", "9"]]
     ),
    (["TEN", "TWO", "ONE"],
     [["O", "1"], ["T", "0"], ["W", "9"],
      ["E", "5"], ["N", "4"]]
     ),
    (["ONE", "ONE", "TWO"],
     [["O", "2"], ["T", "4"], ["W", "6"],
      ["E", "1"], ["N", "3"]]
     ),
    (["ONE", "ONE", "TWO"],
     [["O", "0"], ["T", "1"], ["W", "2"], ["E", "5"], ["N", "6"]]
     ),
    (["A", "A", "A"],
     [["A", "0"]]
     ),
    (["A", "B", "C"],
     [["A", "5"], ["B", "6"], ["C", "1"]]
     ),
    (["AA", "AA", "AA"],
     [["A", "0"]]
     ),
    (["A", "A", "A"],
     [["A", "1"]]
     ),
    (["AA", "AA", "BB"],
     [["A", "1"], ["B", "2"]]
     ),
    (["BAA", "CAB", "DAB"],
     [["A", "0"], ["B", "1"], ["C", "2"], ["D", "4"]]
     ),
]

t_my = Timer("runner(myIsCryptSolution, inputs)", globals=globals())
t_tv = Timer("runner(tvIsCryptSolution, inputs)", globals=globals())
t_tv2 = Timer("runner(tv2IsCryptSolution, inputs)", globals=globals())
t_f = Timer("runner(fastest, inputs)", globals=globals())

runner(myIsCryptSolution, inputs)

r_times = 5
n_times = 10000

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t_tv2.repeat(r_times, n_times))))
print('f  : {:.10f}'.format(min(t_f.repeat(r_times, n_times))))
