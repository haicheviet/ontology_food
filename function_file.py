import random
import itertools
import re

def find_type(list_food, types):
    result = {}
    for food in list_food:
        if list_food[food][0] == types:
            result[food] = list_food[food]
    return result

#rule_meal = [0.1, 1]


def caculate_gram(rule_meal, calor_food, calor_per_meal):  # return
    result = None

    calor_food_for_meal = round(rule_meal[0] * calor_per_meal, 2)
    portion = round(calor_food_for_meal / calor_food * 100, 1)

    result = [calor_food_for_meal, portion]
    return result


def food_not_use_together(list_food, meal):
    list_food_name = []
    list_food_not_use = set()
    for item in meal:
        for food_name in item:
            list_food_name.append(food_name)
            food_not_use = re.findall(r'\[(.*?)\]', list_food[food_name][2])
            if food_not_use != []:
                food_not_use = food_not_use[0].split(",")
                food_not_use = list(
                    map(lambda x: x.replace("'", ""), food_not_use))
                for item in food_not_use:
                    list_food_not_use.add(item.strip())
    # print(list_food_name,  "list_food_not_use", list_food_not_use)
    for food in list_food_name:
        if food in list_food_not_use:
            return False
    return True


def nCi(n_array, number):
    result = None

    result = list(itertools.combinations(n_array, number))
    return result

def caculate_menu_score(menu, list_food):
    score_real = 0
    score_abstract = 0
    confident = None
    ideal_score = 2
    for meal in menu:
        for item in meal:
            for food in item:
                score_real += list_food[food][3] # food_score
                score_abstract += ideal_score
     
    confident = round(score_real / score_abstract * 100, 2)
    menu = (menu, confident)
    return menu