# -*- coding: utf-8 -*-
import sys
import os
import json
import re


with open("result_after_clean.json", 'r')as f:
    search = json.load(f)

#
# ─── QUERY DEF ──────────────────────────────────────────────────────────────────
#


# {'label': 'Táo', 'type': 'Fruits', 'has_calo': '52'}
def food_attribute(label):
    result = {"label": label, "Has_Nutrient": [],"Not_Use_Together": []}


    for content in search:
        if content["label"] == label and content['p'] == "type" and content['o'] != "NamedIndividual":
            result["type"] = content['o']
            target_index = search.index(content)
            text_tamp_next = search[target_index:]
            break
    for content in text_tamp_next:
        if content["label"] == label:
            if content['p'] != "Has_Nutrient" and content['p'] != "Not_Use_Together":
                result[content['p']] = content['o']
            else:
                result[content['p']].append(content['o'])
    return result


# {'label': '35.00-39.99', 'type': 'Body_Mass_Index_Range', 'value': 'Béo_phì_độ_2'}
def has_value(label):
    result = {}
    result["label"] = label
    for content in search:
        if content["label"] == label and content['p'] == "type" and content['o'] != "NamedIndividual":
            result["type"] = content['o']
            target_index = search.index(content)
            text_tamp_next = search[target_index:]
            break
    if result["type"] == "Physical_Activity_Level":
        for content in text_tamp_next:
            if content["label"] == label and content["p"] == "Has_Activity_Level_Range":
                result["value"] = content['o']
    elif result["type"] == "Body_Mass_Index_Range":
        for content in text_tamp_next:
            if content["label"] == label and content["p"] == "Has_Body_Mass_Index_Level":
                result["value"] = content['o']
    return result

# def BMI_value_calc(height,weight):


def BMI_range_calc(value):
    if value == 40:
        return "40.00"

    result = []
    tamp = None
    for content in search:
        if content['p'] == "type" and content['o'] == 'Body_Mass_Index_Range':
            tamp = content["label"]
            try:
                result.append(list(map(float, tamp.split("-"))))
            except:
                pass
    for content in result:
        if content[0] <= value <= content[1]:
            tamp = content
    result = "{0:.2f}-{1:.2f}".format(tamp[0], tamp[1])
    return result


def BMI_level_calc(range):  # Thiếu_cân_rất_nặng
    return has_value(range)["value"]


def extract_person_information(person):
    result = {}
    result["Person"] = person
    for content in search:
        if content["label"] == person and content["p"] != "type":
            result[content['p']] = content['o']
    return result


def check_individual_exist(name):
    flag = True
    for content in search:
        if content["label"] == name and content["o"] == "NamedIndividual":
            flag = False
            break
    return flag

# def ListStructureOfBreakFast():


def avoided_group_food(illness):
    group_food = []
    result = []
    for content in search:
        if content["label"] == illness and content["p"] == "Avoid_Group_Food":
            group_food .append(content["o"])
    for food_item in group_food:
        for content in search:
            if content["label"] == food_item and content["p"] == "Has_Food":
                result.append(content["o"])
    return result


def needed_group_food(illness):
    group_food = []
    result = []
    for content in search:
        if content["label"] == illness and content["p"] == "Need_Group_Food":
            group_food .append(content["o"])
        if content["label"] == illness and content["p"] == "Need_Food":
            result.append(content["o"])
    for food_item in group_food:
        for content in search:
            if content["label"] == food_item and content["p"] == "Has_Food":
                result.append(content["o"])
    return result


def limit_food(illness):
    result = []
    for content in search:
        if content["label"] == illness and content["p"] == "Limit_Food":
            result.append(content["o"])
    return result


def all_food():
    types = []
    result = []
    for content in search:
        if content["p"] == "subClassOf" and content["o"] == "Food_Items":
            types.append(content["label"])
    for content in search:
        if content["p"] == "type" and (content["o"] in types):
            food_attrb = food_attribute(content["label"])

            try:
                if food_attrb["Not_Use_Together"] != []: 
                    result.append(str(food_attrb["label"]) + "|" + str(food_attrb["type"]) + "|" +
                                str(food_attrb["Has_calo"]) + "|" + str(food_attrb["Not_Use_Together"]))
                else: result.append(str(food_attrb["label"]) + "|" + str(food_attrb["type"]) + "|" +
                                str(food_attrb["Has_calo"]) + "|")
            except:
                pass
    return result


# [0.4,Cereal,1];[0.2,Dairy_Products,1];[0.3,Fruit,1]
def condtion_for_rule_meal(food_default, list_only_food):
    result = []
    for food in food_default:
        if food in list_only_food:
            result.append(food)
    return result

def destructure_rule_meal(content, list_only_food):
    result = {}
    food_list = re.findall(r'\[(.*?)\]', content)
    print(food_list)
    for food_attrb in food_list:
        food = food_attrb.split(",")
        if "{" in food[1]:
            food[1] = food[1].replace("}", "")
            food_default = food[1].split("{")[1]
            food_default = food_default.split("|")
            # return result{"fix": ["food_name", "portion", "quanity"]}
            result["fix"] = [condtion_for_rule_meal(food_default, list_only_food)
                             ,float(food[0]), int(food[2])]
        else:
            result[food[1]] = [float(food[0]), int(food[2])]
    return result

def list_structure_breakfast(list_food):
    list_rule = []
    for content in search:
        if content["label"] == 'StructureOfBreakfast' and content["p"] == "Has_structure":
            list_rule.append(destructure_rule_meal(content["o"], list_food))
    return list_rule


def list_structure_dinner(list_food):
    list_rule = []
    for content in search:
        if content["label"] == 'StructureOfDinner' and content["p"] == "Has_structure":
            list_rule.append(destructure_rule_meal(content["o"], list_food))
    return list_rule


def list_structure_lunch(list_food):
    list_rule = []
    for content in search:
        if content["label"] == 'StructureOfLunch' and content["p"] == "Has_structure":
            print(content['o'])
            list_rule.append(destructure_rule_meal(content["o"], list_food))
    return list_rule


if __name__ == "__main__":
    print(avoided_group_food("Bệnh_béo_phì")) 
