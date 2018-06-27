# -*- coding: utf-8 -*-
import sys
import os
import json


with open("result_after_clean.json", 'r')as f:
    search = json.load(f)

#
# ─── QUERY DEF ──────────────────────────────────────────────────────────────────
#

# {'label': 'Táo', 'type': 'Fruits', 'Has_calo': '52'}


def food_attribute(label):
    result = {}
    result["label"] = label
    result["Has_Nutrient"] = []
    for content in search:
        if content["label"] == label and content['p'] == "type" and content['o'] != "NamedIndividual":
            result["type"] = content['o']
            target_index = search.index(content)
            text_tamp_next = search[target_index:]
            break
    for content in text_tamp_next:
        if content["label"] == label:
            if content['p'] != "Has_Nutrient":
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

if __name__ == "main":
    print(BMI_level_calc('0.00-15.99'))
