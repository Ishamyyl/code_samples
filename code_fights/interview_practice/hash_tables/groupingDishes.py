""" You have a list of dishes. Each dish is associated with a list of ingredients used to prepare it.
You want to group the dishes by ingredients, so that for each ingredient you'll be able to find all the dishes
that contain it (if there are at least 2 such dishes).

Return an array where each element is a list with the first element equal to the name of the ingredient
and all of the other elements equal to the names of dishes that contain this ingredient.
The dishes inside each list should be sorted lexicographically. The result array should be sorted lexicographically
by the names of the ingredients in its elements.

my : 0.3810753500
tv : 0.3841263129
tv2: 0.4155840157
"""
from timeit import Timer
from pprint import pprint
from collections import defaultdict


def myGroupDishes(dishes):
    d = defaultdict(set)
    t = [(i, k) for k, *ing in dishes for i in ing]
    for k, v in t:
        d[k].add(v)
    return sorted([k] + sorted(v) for k, v in d.items() if len(v) > 1)


def tvGroupingDishes(dishes):
    groups = {}
    for d, *v in dishes:
        for x in v:
            groups.setdefault(x, []).append(d)
    ans = []
    for x in sorted(groups):
        if len(groups[x]) >= 2:
            ans.append([x] + sorted(groups[x]))
    return ans


def tv2GroupingDishes(dishes):
    ingredients = {}
    for dish in dishes:
        name, *parts = dish
        for part in parts:
            ingredients[part] = ingredients.get(part, [])
            ingredients[part].append(name)
    return [[ingredient] + sorted(ingredients[ingredient]) for ingredient in sorted(ingredients) if len(ingredients[ingredient]) > 1]


def runner(func, inputs):
    list(map(func, inputs))


inputs = [
    [["Salad", "Tomato", "Cucumber", "Salad", "Sauce"],
     ["Pizza", "Tomato", "Sausage", "Sauce", "Dough"],
     ["Quesadilla", "Chicken", "Cheese", "Sauce"],
     ["Sandwich", "Salad", "Bread", "Tomato", "Cheese"]],
    [["Pasta", "Tomato Sauce", "Onions", "Garlic"],
     ["Chicken Curry", "Chicken", "Curry Sauce"],
     ["Fried Rice", "Rice", "Onions", "Nuts"],
     ["Salad", "Spinach", "Nuts"],
     ["Sandwich", "Cheese", "Bread"],
     ["Quesadilla", "Chicken", "Cheese"]],
    [["Pasta", "Tomato Sauce", "Onions", "Garlic"],
     ["Chicken Curry", "Chicken", "Curry Sauce"],
     ["Fried Rice", "Rice", "Onion", "Nuts"],
     ["Salad", "Spinach", "Nut"],
     ["Sandwich", "Cheese", "Bread"],
     ["Quesadilla", "Chickens", "Cheeseeee"]],
    [["First", "a", "b", "c", "d", "e", "f", "g", "h", "i"],
     ["Second", "i", "h", "g", "f", "e", "x", "c", "b", "a"]]
]

t_my = Timer("runner(myGroupDishes, inputs)", globals=globals())
t_tv = Timer("runner(tvGroupingDishes, inputs)", globals=globals())
t_tv2 = Timer("runner(tv2GroupingDishes, inputs)", globals=globals())

r_times = 5
n_times = 10000

print('my : {:.10f}'.format(min(t_my.repeat(r_times, n_times))))
print('tv : {:.10f}'.format(min(t_tv.repeat(r_times, n_times))))
print('tv2: {:.10f}'.format(min(t_tv2.repeat(r_times, n_times))))
