""" Given an array strings, determine whether it follows the sequence given in the patterns array.
In other words, there should be no i and j
for which strings[i] = strings[j] and patterns[i] ≠ patterns[j]
or for which strings[i] ≠ strings[j] and patterns[i] = patterns[j].

my : 0.2273704991
tv : 0.3360737439
tv2: 0.4916709994
"""
from timeit import Timer
from itertools import starmap


def myAreFollowingPatterns(strings, patterns):
    mapping = {}
    for s, p in zip(strings, patterns):
        if s not in mapping:
            mapping[s] = p
        else:
            if mapping[s] != p:
                return False
    v = mapping.values()
    if len(v) != len(set(v)):
        return False
    return True


def tvAreFollowingPatterns(strings, patterns):
    """ The ACTUAL top-voted answer is

            def areFollowingPatterns(strings, patterns):
                d = {}
                for i, j in zip(strings, patterns):
                    if i in d and d[i] != j:
                        return False
                    d[i] = j
                return len(d) == len(set(d.values()))

        but it's basically identical to my answer so I didn't include it. Also, it runs slightly slower.
    """
    bs = dict()
    for i in range(len(strings)):
        if strings[i] in bs:
            if bs[strings[i]] != patterns[i]:
                return False
        else:
            bs[strings[i]] = patterns[i]
    return len(bs.values()) == len(set(patterns))


def tv2AreFollowingPatterns(strings, patterns):
    a = dict(zip(patterns, strings))
    b = dict(zip(strings, patterns))
    if len(a) != len(b):
        return False
    for i in range(len(patterns)):
        if a[patterns[i]] != strings[i]:
            return False
    return True


def runner(func, inputs):
    list(starmap(func, inputs))


inputs = [
    [["cat", "dog", "dog"],
     ["a", "b", "b"]],
    [["cat", "dog", "doggy"],
     ["a", "b", "b"]],
    [["cat", "dog", "dog"],
     ["a", "b", "c"]],
    [["aaa"],
     ["aaa"]],
    [["aaa", "aaa", "aaa"],
     ["aaa", "bbb", "aaa"]],
    [["aaa", "aab", "aaa"],
     ["aaa", "aaa", "aaa"]],
    [["re", "jjinh", "rnz", "frok", "frok", "hxytef", "hxytef", "frok"],
     ["kzfzmjwe", "fgbugiomo", "ocuijka", "gafdrts", "gafdrts", "ebdva", "ebdva", "gafdrts"]],
    [["kwtfpzm", "kwtfpzm", "kwtfpzm", "kwtfpzm", "kwtfpzm", "wfktjrdhu", "anx", "kwtfpzm"],
     ["z", "z", "z", "hhwdphhnc", "zejhegjlha", "xgxpvhprdd", "e", "u"]],
    [["ato", "ato", "jflywws", "ato", "ato", "se", "se", "kiolm", "wizdkdqke"],
     ["ofnmiqelt", "ofnmiqelt", "flqmwoje", "ofnmiqelt", "zdohw", "jyk", "ujddjtxt", "s", "kw"]],
    [["syf", "syf", "oxerkx", "oxerkx", "syf", "xgwatff", "pmnfaw", "t", "ajyvgwd", "xmhb", "ajg", "syf",
      "syf", "wjddgkopae", "fgrpstxd", "t", "i", "psw", "wjddgkopae", "wjddgkopae", "oxerkx", "zf", "jvdtdxbefr",
      "rbmphtrmo", "syf", "yssdddhyn", "syf", "jvdtdxbefr", "funnd", "syf", "syf", "wd", "syf", "vnntavj", "wjddgkopae",
      "yssdddhyn", "wcvk", "wjddgkopae", "fh", "zf", "gpkdcwf", "qkbw", "zf", "teppnr", "jvdtdxbefr", "fmn",
      "i", "hzmihfrmq", "wjddgkopae", "syf", "vnntavj", "dung", "kn", "qkxo", "ajyvgwd", "fs", "kanixyaepl",
      "syf", "tl", "yzhaa", "dung", "wa", "syf", "jtucivim", "tl", "kanixyaepl", "oxerkx", "wjddgkopae", "ey",
      "ai", "zf", "di", "oxerkx", "dung", "i", "oxerkx", "wmtqpwzgh", "t", "beascd", "me", "akklwhtpi", "nxl", "cnq",
      "bighexy", "ddhditvzdu", "funnd", "wmt", "dgx", "fs", "xmhb", "qtcxvdcl", "thbmn", "pkrisgmr", "mkcfscyb",
      "x", "oxerkx", "funnd", "iesr", "funnd", "t"],
     ["enrylabgky", "enrylabgky", "dqlqaihd", "dqlqaihd", "enrylabgky", "ramsnzhyr", "tkibsntkbr", "l", "bgtws",
      "xwuaep", "o", "enrylabgky", "enrylabgky", "e", "auljuhtj", "l", "d", "jfzokgt", "e", "e", "dqlqaihd",
      "fgglhiedk", "nj", "quhv", "enrylabgky", "oadats", "enrylabgky", "nj", "zwupro", "enrylabgky", "enrylabgky", "pyw",
      "enrylabgky", "bedpuycdp", "e", "oadats", "i", "e", "fobyfznrxm", "fgglhiedk", "irxtd", "oyvf", "fgglhiedk", "ebpp",
      "nj", "p", "d", "cufxylz", "e", "enrylabgky", "bedpuycdp", "mitzb", "shsnw", "papmvh", "bgtws", "chtp", "pze",
      "enrylabgky", "klp", "wpx", "mitzb", "fo", "enrylabgky", "bvcigrirhe", "klp", "pze", "dqlqaihd", "e", "iufunacwjo",
      "bubgww", "fgglhiedk", "og", "dqlqaihd", "mitzb", "d", "dqlqaihd", "mysidv", "l", "naj", "clftmrwl",
      "fjb", "zjjnrffb", "sh", "gcn", "ouispza", "zwupro", "c", "rdank", "chtp", "xwuaep", "jufhm", "iyntbgm",
      "sufs", "mkivpe", "bxdd", "dqlqaihd", "zwupro", "vzxbbculgv", "zwupro", "l"]],
]

t_my = Timer("runner(myAreFollowingPatterns, inputs)", globals=globals())
t_tv = Timer("runner(tvAreFollowingPatterns, inputs)", globals=globals())
t_tv2 = Timer("runner(tv2AreFollowingPatterns, inputs)", globals=globals())

r_times = 5
n_times = 10000

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t_tv2.repeat(r_times, n_times))))
