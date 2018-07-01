import sys
import os
import re
from query_rdfs import *
import itertools
import random

sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
current_dir = os.path.dirname("__file__")
current_dir = current_dir if current_dir is not '' else '.'
# directory to scan for any txt files
data_dir_path = current_dir + '/rule'

known = {"name": "Che Viet Hai", "height": 170, "weight": 55, "gender": "nam",
         "age": 17, "PhysicalActiveLevel": "Hoạt động vừa", "target": "giữ cân",
         "ListIllness": "Bệnh_béo_phì"}
data_rule = []
function = []
with open(data_dir_path + "/rule.txt", "r", encoding="utf8") as f:
    for line in f:
        data_rule.append(line)
with open(data_dir_path + "/function.txt", "r", encoding="utf8") as f:
    for line in f:
        function.append(line)


#
# ─── --- ────────────────────────────────────────────────────────────────────────
#

def BMIvalueCalc(height, weight):
    height /= 100
    return round(eval(function[2].split("=")[1]), 2)


def BMIrangeCalc(bmi_value):
    return BMI_range_calc(bmi_value)


def BMIlevelCalc(bmi_range):
    return has_value(bmi_range)["value"]

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def BMRvalueOfMaleCalc(height, weight, age):
    function[1] = function[1].split("=")[1]
    return round(eval(function[1]), 2)


def BMRvalueOfFemaleCalc(height, weight, age):
    function[1] = function[1].split("=")[1]
    return round(eval(function[1]), 2)

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def PAvalueCalc(PhysicalActiveLevel):
    for count in range(4, 9):
        result = function[count].split(":")
        if result[1].endswith("\n"):
            result[1] = result[1][:-1]
        if result[1] == PhysicalActiveLevel:
            return float(result[0])

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def CaloCalc(BMRvalue, PhysicalActiveValue, target):
    result = round(eval(function[3].split("=")[1]), 2)
    if target == "tăng cân":
        result += 500
    elif target == "giảm cân":
        result -= 500
    return result

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def CaloToKeepWeightCalc(calo_per_day):
    # breakfast: 26%, #Lunch: 40%, # Dinner: 34%
    return [round(calo_per_day*26/100, 2),
            round(calo_per_day*40/100, 2), round(calo_per_day*34/100, 2)]

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def FindAvoidFood(list_illness):
    return avoided_group_food(list_illness)  # return array


def FindNeedFood(list_illness):
    return needed_group_food(list_illness)


def FindLimitFood(list_illness):
    return limit_food(list_illness)


def FilterFood(list_avoid_food, list_need_food,
               list_limit_food):
    result = {}
    list_all_food = []
    tamp_list = [food.split("|") for food in all_food()]
    set_avoid_food = set(list_avoid_food)
    for food in tamp_list:
        if food[0] not in set_avoid_food:
            list_all_food.append(food)
    for food_1 in list_all_food:
        if food_1[0] in list_need_food:
            food_1.append(1)
            result[food_1[0]] = food_1[1:]
        elif food_1[0] in list_limit_food:
            food_1.append(-1)
            result[food_1[0]] = food_1[1:]
        else:
            food_1.append(0)
            result[food_1[0]] = food_1[1:]
    return result

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def extract_rule_left(rule_left):
    rule_left = re.findall(r'\[(.*?)\]', rule_left)
    flag = True
    for content in rule_left:
        content = content.split(",")
        if content[0] == "1":
            if content[1] not in known:
                flag = False
                break
        elif content[0] == "2":
            try:
                if known[content[1]] != content[2]:
                    flag = False
                    break
            except:
                flag = False
                break
    return flag


def extract_rule_right(rule_right):
    rule_right = rule_right.split(",", 1)
    flag = True
    rule_right[0] = rule_right[0][1:]
    rule_right[1] = rule_right[1][:-2]
    if rule_right[0] in known:
        flag = False
    else:
        funct = rule_right[1].split(':')[1]
        known[rule_right[0]] = eval(funct)
    return flag


def extract_rule(rule):
    flag = True
    rule_left, rule_right = rule.split("|")
    flag = extract_rule_left(rule_left)
    if flag is False:
        return flag
    else:
        flag = extract_rule_right(rule_right)
    return flag

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def update_known(data_rule):
    count = 0
    while count <= 13:
        if extract_rule(data_rule[count]) == True:
            print("True")
            count = 0
    else:
        count += 1


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
    for food in list_food_name:
        if food in list_food_not_use:
            return False
    return True


def nCi(n_array, number):
    result = None

    result = list(itertools.combinations(n_array, number))
    return result

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def FindListBreakFast(data):
    # Declear variable
    list_food = data["ListFood"]
    calor_each_meal = data["CaloForEachMeal"][0]
    # print("BreakFast: ", calor_each_meal)
    result = []
    food_fix = {}
    food_next = []
    structure_breakfast = list_structure_breakfast(list_food)

    element = random.choice(structure_breakfast)
    # print("element: ", element)
    units = {}
    for key in element:
        if key == "fix":
            if len(element["fix"][0]) == 1:
                food_name = element[key][0][0]
                rule = element[key][1:]
                calor_food = float(list_food[food_name][1])
                food_fix[food_name] = caculate_gram(
                    rule, calor_food, calor_each_meal)
        else:
            types = key
            rule = element[key]
            # print(types)
            list_food_types = find_type(list_food, types)
            sorted_by_value = dict(sorted(list_food_types.items(),
                                          key=lambda kv: kv[1][3], reverse=True))
            best_food = []
            for count, units in enumerate(sorted_by_value):
                if count > 2:
                    break
                else:  # pick three foods have best score
                    best_food.append(units)
            combination = nCi(best_food, rule[1])
            # print(combination)
            for index, element_combination in enumerate(combination):
                tamp = {}
                for food_name in element_combination:
                    calor_food = float(list_food[food_name][1])
                    tamp[food_name] = caculate_gram(
                        rule, calor_food, calor_each_meal)
                    combination[index] = tamp
            food_next.append(combination)

    # create result
    food_next.append([food_fix])
#     print('food_next: ', food_next)
    tamp = list(itertools.product(*food_next))
    # print(len(tamp))
    for item in tamp:
        if food_not_use_together(list_food, item):
            result.append(item)
    return result


def FindListDinner(data):
    # Declear variable
    list_food = data["ListFood"]
    calor_each_meal = data["CaloForEachMeal"][2]
    # print("Dinner: ", calor_each_meal)
    result = []
    food_fix = {}
    food_next = []
    structure_dinner = list_structure_dinner(list_food)

    element = random.choice(structure_dinner)
    # print("element: ", element)
    units = {}
    for key in element:
        if key == "fix":
            if len(element["fix"][0]) == 1:
                food_name = element[key][0][0]
                rule = element[key][1:]
                calor_food = float(list_food[food_name][1])
                food_fix[food_name] = caculate_gram(
                    rule, calor_food, calor_each_meal)
        else:
            types = key
            rule = element[key]
            # print(types)
            list_food_types = find_type(list_food, types)
            sorted_by_value = dict(sorted(list_food_types.items(),
                                          key=lambda kv: kv[1][3], reverse=True))
            best_food = []
            for count, units in enumerate(sorted_by_value):
                if count > 2:
                    break
                else:  # pick three foods have best score
                    best_food.append(units)
            combination = nCi(best_food, rule[1])
            # print(combination)
            for index, element_combination in enumerate(combination):
                tamp = {}
                for food_name in element_combination:
                    calor_food = float(list_food[food_name][1])
                    tamp[food_name] = caculate_gram(
                        rule, calor_food, calor_each_meal)
                    combination[index] = tamp
            food_next.append(combination)

    # create result
    food_next.append([food_fix])
#     print('food_next: ', food_next)
    tamp = list(itertools.product(*food_next))
    # print(len(tamp))
    for item in tamp:
        if food_not_use_together(list_food, item):
            result.append(item)
    return result


def FindListLunch(data):
    # Declear variable
    list_food = data["ListFood"]
    calor_each_meal = data["CaloForEachMeal"][1]
    # print("lunch: ", calor_each_meal)
    result = []
    food_fix = {}
    food_next = []
    structure_lunch = list_structure_lunch(list_food)

    element = random.choice(structure_lunch)
    # print("element: ", element)
    units = {}
    for key in element:
        if key == "fix":
            if len(element["fix"][0]) == 1:
                food_name = element[key][0][0]
                rule = element[key][1:]
                calor_food = float(list_food[food_name][1])
                food_fix[food_name] = caculate_gram(
                    rule, calor_food, calor_each_meal)
        else:
            types = key
            rule = element[key]
#             print(types)
            list_food_types = find_type(list_food, types)
            sorted_by_value = dict(sorted(list_food_types.items(),
                                          key=lambda kv: kv[1][3], reverse=True))
            best_food = []
            for count, units in enumerate(sorted_by_value):
                if count > 2:
                    break
                else:  # pick three foods have best score
                    best_food.append(units)
            combination = nCi(best_food, rule[1])
#             print(combination)
            for index, element_combination in enumerate(combination):
                tamp = {}
                for food_name in element_combination:
                    calor_food = float(list_food[food_name][1])
                    tamp[food_name] = caculate_gram(
                        rule, calor_food, calor_each_meal)
                    combination[index] = tamp
            food_next.append(combination)

    # create result
    food_next.append([food_fix])
#     print('food_next: ', food_next)
    tamp = list(itertools.product(*food_next))
    for item in tamp:
        if food_not_use_together(list_food, item):
            result.append(item)
    return result

def JoinMeal(breakfast_list, lunch_list, dinner_list):
    result = None
    food = [breakfast_list, lunch_list, dinner_list]
    result = list(itertools.product(*food))

    print(len(result))
    return result

if __name__ == "__main__":
    count = 0
    while count <= 13:
        if extract_rule(data_rule[count]) == True:
            print("True")
            count = 0
        else:
            count += 1
    print("------------------")
    print('known: ', known)
    print("--------------------")

    breakfast_list = FindListBreakFast(known)
    lunch_list = FindListLunch(known)
    dinner_list = FindListDinner(known)
    menu = JoinMeal(breakfast_list, lunch_list, dinner_list)
    print(menu[0])
    for i in menu[0]:
        print('i', i)
