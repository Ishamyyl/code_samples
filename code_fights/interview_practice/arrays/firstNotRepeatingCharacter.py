""" Given a string s, find and return the first instance of a non-repeating character in it.
If there is no such character, return '_'.

Note: Write a solution that only iterates over the string once and uses O(1) additional memory,
since this is what you would be asked to do during a real interview.

my : 0.3427834787
tv : 0.9100127241
tv2: 0.7164314174
"""
from collections import OrderedDict
from timeit import Timer


def myFirstNotRepeatingCharacter(s):
    c = OrderedDict()
    for i in s:
        if i in c:
            c[i] += 1
        else:
            c[i] = 1
    for k, v in c.items():
        if v == 1:
            return k
    return '_'


def tvFirstNotRepeatingCharacter(s):
    letters = []
    flag = [False] * 26
    for ch in s:
        if flag[ord(ch) - ord('a')]:
            if ch in letters:
                letters.remove(ch)
        else:
            letters.append(ch)
            flag[ord(ch) - ord('a')] = True
    if len(letters) == 0:
        return '_'
    else:
        return letters[0]


def tv2FirstNotRepeatingCharacter(s):
    c = []
    x = set()
    for i in s:
        if i not in c:
            c.append(i)
        else:
            x.add(i)
    for i in x:
        c.remove(i)
    if c == []:
        return '_'
    return c[0]


def runner(func, inputs):
    list(map(func, inputs))


inputs = [
    "abacabad",
    "abacabaabacaba",
    "z",
    "bcb",
    "bcccccccb",
    "abcdefghijklmnopqrstuvwxyziflskecznslkjfabe",
    "zzz",
    "bcccccccccccccyb",
    "xdnxxlvupzuwgigeqjggosgljuhliybkjpibyatofcjbfxwtalc",
    "ngrhhqbhnsipkcoqjyviikvxbxyphsnjpdxkhtadltsuxbfbrkof",
]

t_my = Timer("runner(myFirstNotRepeatingCharacter, inputs)", globals=globals())
t_tv = Timer("runner(tvFirstNotRepeatingCharacter, inputs)", globals=globals())
t2_tv = Timer("runner(tv2FirstNotRepeatingCharacter, inputs)", globals=globals())

r_times = 5
n_times = 10000

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t2_tv.repeat(r_times, n_times))))
