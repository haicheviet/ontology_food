import sys
import os
import re
from operator import itemgetter
from query_rdfs import *
import itertools
import random
from function_file import *

sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
current_dir = os.path.dirname("__file__")
current_dir = current_dir if current_dir is not '' else '.'
# directory to scan for any txt files
data_dir_path = current_dir + '/rule'

with open(current_dir + "/Information_user/known.json",'r', encoding = 'utf8') as lst:
    known = json.load(lst)

known_tamp = known
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
    result = function[1].split("=")[1]
    return round(eval(result), 2)


def BMRvalueOfFemaleCalc(height, weight, age):
    result = function[0].split("=")[1]
    return round(eval(result), 2)

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

def CaloToGainWeightCalc(calo_per_day):
    # breakfast: 26%, #Lunch: 40%, # Dinner: 34%
    return [round(calo_per_day*26/100, 2),
            round(calo_per_day*40/100, 2), round(calo_per_day*34/100, 2)]

def CaloToLoseWeightCalc(calo_per_day):
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
               list_limit_food, list_unlike_food):
    result = {}
    list_all_food = []
    tamp_list = [food.split("|") for food in all_food()]
    set_avoid_food = set(list_avoid_food)
    for item in list_unlike_food:
        set_avoid_food.add(item)
    for food in tamp_list:
        if food[0] not in set_avoid_food:
            list_all_food.append(food)
    for food_1 in list_all_food:
        if food_1[0] in list_need_food:
            food_1.append(2)
            result[food_1[0]] = food_1[1:]
        elif food_1[0] in list_limit_food:
            food_1.append(0)
            result[food_1[0]] = food_1[1:]
        else:
            food_1.append(1)
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
    # print(rule)
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


def JoinMeal(breakfast_list, lunch_list, dinner_list, list_food):
    result = None
    food = [breakfast_list, lunch_list, dinner_list]
    result = list(itertools.product(*food))

    for count, menu in enumerate(result):
        menu = caculate_menu_score(menu, list_food)
        result[count] = menu

    result.sort(key = itemgetter(1), reverse = True)
    print(len(result))

    return result

def main():
    count = 0
    while count <= 13:
        # print(data_rule[count])
        if extract_rule(data_rule[count]) == True:
            # print("True")
            count = 0
            continue
        else:
            # print(extract_rule(data_rule[count]))
            count += 1
    # print("------------------")
    # print('known: ', known)
    # print("--------------------")

    breakfast_list = FindListBreakFast(known)
    lunch_list = FindListLunch(known)
    dinner_list = FindListDinner(known)
    menu = JoinMeal(breakfast_list, lunch_list, dinner_list, known["ListFood"])
    result = random.choice(menu[0:7000])
    return result

if __name__ == "__main__":
    try:
        print(sys.argv[1])
        print("start_function_1")
        tamp = main()
        data = open(current_dir + "/Information_user/status_health.txt", 'w', encoding = 'utf8')
        # print(known['BMIlevel'])
        # print("ss")
        data.write(str(known['BMIlevel']) + '\n' + str(known['BMRvalue']) + '\n' + str(known["CaloPerDay"]))
        print("--------------------------------")
        data.close()
        print("done")

    except Exception as v:
        print(v)
        try:
            print("start_function_2")
            menu_list = []

            for i in range(0,5):
                menu_list.append(main())
                known = known_tamp
        except Exception as e:
            print('Failed to do something: ' + str(e))
            print(known)
        for count, menu in enumerate(menu_list):
            f = open(current_dir + "/menu_list/menu_%s.txt" %count, 'w', encoding = 'utf8')
            for count, element_list in enumerate (menu):
                if count!=1:
                    try:
                        for element in element_list:
                            for item in element:
                                for food in item:
                                    f.write(str(food) + " " + " ".join(list(map(str, item[food]))) + '\n')
                            f.write("\n")
                    except Exception as e:
                        print('count', count)
                        print ("element: ",  element_list)
                    
                else:
                    f.write(str(element_list))

            f.close()
        print("done")
    
