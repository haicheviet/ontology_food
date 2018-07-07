# -*- coding: utf-8 -*-
import sys
import os
import json
import re

sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
current_dir = os.path.dirname("__file__")
current_dir = current_dir if current_dir is not '' else '.'
# directory to scan for any owl files
data_dir_path = current_dir + '/data_after_clean'


with open(data_dir_path + "/result_after_clean.json", 'r')as f:
    search = json.load(f)

#
# ─── QUERY DEF ──────────────────────────────────────────────────────────────────
#

def illness_list():
    result = []
    for content in search:
        if content["p"] == "type" and content["o"] == "Illness":
            result.append(content["label"])

    return result

def all_food():
    result = []

    for content in search:
        if content["p"] == "Has_calo":
            food_attrb = food_attribute(content["label"])
            try:
                if food_attrb["Not_Use_Together"] != []:
                    result.append(str(food_attrb["label"]) + "|" + str(food_attrb["type"]) + "|" +
                                    str(food_attrb["Has_calo"]) + "|" + str(food_attrb["Not_Use_Together"]))
                else:
                    result.append(str(food_attrb["label"]) + "|" + str(food_attrb["type"]) + "|" +
                                    str(food_attrb["Has_calo"]) + "|")
            except:
                pass
            
    return result

def food_nutrient():
    food = []
    nutrient = []
    for content in search:
        if content["p"] == "Has_calo":
            food.append(content["label"])

    for content in search:
        if content['p'] == "Has_lack_of_sb_effect":
            nutrient.append(content["label"])
    return food, nutrient

def food_type():
    types = []
    for content in search:
        if content["p"] == "subClassOf" and content["o"] == "Food_Items":
            types.append(content["label"])
    return types

def nutrient_type():
    types = []
    for content in search:
        if content["p"] == "subClassOf" and content["o"] == "Nutrients":
            types.append(content["label"])
    return types

def food_calo():
    result = {}

    for content in search:
        if content['p'] == "Has_calo":
            result[content['label']] = content['o']
    return result

def menu_list():
    result = []
    for content in search:
        if content['p'] == "type" and content['o'] == 'Menu':
            result.append(content['label'])

    return result

#
# ─── ---- ───────────────────────────────────────────────────────────────────────
#

# {'label': 'Táo', 'type': 'Fruits', 'has_calo': '52'}
def food_attribute(label):
    result = {"label": label, "Has_Nutrient": [], "Not_Use_Together": [], "illness_should_not_use": []}
    text_tamp_next = None
    group_food = None

    for content in search:
        if content["label"] == label and content['p'] == "type" and content['o'] != "NamedIndividual":
            result["type"] = content['o']
            target_index = search.index(content)
            text_tamp_next = search[target_index:]
        elif content["p"] == "Has_Food" and content["o"] == label:
            group_food = content["label"]

    for content in text_tamp_next:
        if content["label"] == label:
            if content['p'] != "Has_Nutrient" and content['p'] != "Not_Use_Together":
                result[content['p']] = content['o']
            else:
                result[content['p']].append(content['o'])
    
    for content in search:
        if content["p"] == "Avoid_Group_Food" and content["o"] == group_food:
            result["illness_should_not_use"].append(content['label'])
    return result

def nutrient_attribute(label):
    result = {"label": label, "food": []}

    for content in search:
        if content["label"] == label and content['p'] == "type" and content['o'] != "NamedIndividual":
            result["type"] = content['o']
            target_index = search.index(content)
            text_tamp_next = search[target_index:]
        elif content["p"] == "Has_Nutrient" and content["o"] == label:
            result["food"].append(content['label'])

    for content in text_tamp_next:
        if content["label"] == label:
            result[content['p']] = (content['o'])
    return result

def class_individual(class_label):
    result = []
    for content in search:
        if content['p'] == "type" and content['o'] == class_label:
            result.append(content['label'])

    return result

def find_food_by_calo(calor_begin, calo_end):
    result = []
    list_food = food_calo()
    for calo in range(calor_begin, calo_end+1):
        for key, value in list_food.items():
            if int(value) == calo:
                result.append(key)
    return result


#   
# ─── --- ────────────────────────────────────────────────────────────────────────
#

    
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

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


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


#
# ─── --- ────────────────────────────────────────────────────────────────────────
#

    
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

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#


def avoided_group_food(illness):
    group_food = []
    result = []
    for content in search:
        if content["label"] == illness and content["p"] == "Avoid_Group_Food":
            group_food .append(content["o"])
        if content["label"] == illness and content["p"] == "Avoid_Food":
            result.append(content["o"])
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

#
# ─── --- ────────────────────────────────────────────────────────────────────────
#

def condtion_for_rule_meal(food_default, list_only_food):
    result = []
    for food in food_default:
        if food in list_only_food:
            result.append(food)
    return result

def destructure_rule_meal(content, list_only_food):
    result = {}
    food_list = re.findall(r'\[(.*?)\]', content)
    for food_attrb in food_list:
        food = food_attrb.split(",")
        if "{" in food[1]:
            food[1] = food[1].replace("}", "")
            food_default = food[1].split("{")[1]
            food_default = food_default.split("|")
            # return result{"fix": ["food_name", "portion", "quanity"]}
            result["fix"] = [condtion_for_rule_meal(
                food_default, list_only_food), float(food[0]), int(food[2])]
        else:
            result[food[1]] = [float(food[0]), int(food[2])]
    return result


def list_structure_breakfast(list_food):
    list_rule = []
    for content in search:
        if content["label"] == 'StructureOfBreakFast' and content["p"] == "Has_structure":
            list_rule.append(destructure_rule_meal(
                content["o"], list_food))
    return list_rule

def list_structure_dinner(list_food):
    list_rule = []
    for content in search:
        if content["label"] == 'StructureOfDinner' and content["p"] == "Has_structure":
            list_rule.append(destructure_rule_meal(
                content["o"], list_food))
    return list_rule


def list_structure_lunch(list_food):
    list_rule = []
    for content in search:
        if content["label"] == 'StructureOfLunch' and content["p"] == "Has_structure":
            list_rule.append(destructure_rule_meal(
                content["o"], list_food))
    return list_rule

def main_query():
    food, nutrient =  food_nutrient()
    if sys.argv[1] == "food_nutrient()":
        food, nutreint = eval(sys.argv[1])
        f = open(current_dir + "/search/food.txt", 'w', encoding = 'utf8')
        n = open(current_dir + "/search/nutrient.txt", 'w', encoding = 'utf8')
        for food_name in food:
            f.write(food_name + '\n')
        
        for nutrient_name in nutreint:
            n.write(nutrient_name + '\n')
        print("done")
        n.close()
        f.close()
    elif sys.argv[1] in food: #print food_attribute
        command = "food_attribute('%s')" %sys.argv[1]
        result = eval(command)
        try:
            f = open(current_dir + "/search/item_attribute.txt", 'w', encoding = 'utf8')
            f.write("Tên thực phẩm: " + str(result['label']) + '\n')
            f.write("Loại thực phẩm: " + str(result['type']) + '\n')
            f.write("Calo : " + str(result['Has_calo']) + str("/100g") + '\n')
            f.write("Những chất dinh dưỡng: " + str(", ".join(result['Has_Nutrient'])) + '\n')
            f.write("Thời điểm thích hợp ăn: "+ str(result['Has_suitable_time']) + '\n')
            f.write("Những loại thực phẩm không ăn chung: " + str(", ".join(result['Not_Use_Together'])) + '\n')
            f.write("Cách chế biến: " + str(result['Has_processing']) + '\n')
            f.write("Những bệnh không nên dùng thực phẩm này: " + str(", ".join(result['illness_should_not_use'])) + '\n')
        except:
            pass

        f.close()
        print("done")
    elif sys.argv[1] in nutrient: #print nutrient_attribute
        command = "nutrient_attribute('%s')" %sys.argv[1]
        result = eval(command)
        try:
            f = open(current_dir + "/search/item_attribute.txt", 'w', encoding = 'utf8')
            f.write("Tên chất dinh dưỡng: " + str(result['label']) + '\n')
            f.write("Loại chất dinh dưỡng: " + str(result['type']) + '\n')
            f.write("Tác dụng: " + result['Has_effect'] + '\n')
            f.write("Ảnh hưởng khi thừa: " + result['Has_exceed_effect'] + '\n')
            f.write("Ảnh hưởng khi thiếu: "+ result['Has_lack_of_sb_effect'] + '\n')
            f.write("Những món ăn có chất dinh dưỡng này: " +  str(", ".join(result['food'])) + '\n')
        except:
            pass

        f.close()
        print("done")

    elif sys.argv[1] == "illness_list()": #print illness_líst
        illness_list = eval(sys.argv[1])
        f = open(current_dir + "/search/disease.txt", 'w', encoding = 'utf8')
        for illness_name in illness_list:
            if "?" not in illness_name:
                f.write(str(illness_name) + "\n")
            else: pass
        print("done")
        f.close()

    elif sys.argv[1] == "menu_list()": #print illness_líst
        menu_list = eval(sys.argv[1])
        f = open(current_dir + "/search/menu_list.txt", 'w', encoding = 'utf8')
        for menu_name in menu_list:
            if "?" not in menu_name:
                f.write(str(menu_name) + "\n")
            else: pass
        print("done")
        f.close()

    elif "type" in sys.argv[1]: #print type of class
        command = sys.argv[1]
        list_items = eval(command)
        f = open(current_dir + "/search/%s.txt"%command[:-2], 'w', encoding = 'utf8')
        for item in list_items:
            if "?" not in item:
                f.write(str(item) + '\n')
            else: pass
        print("done")
        f.close()

    elif "class" in sys.argv[1]:
        command = sys.argv[1]
        list_items = eval(command)
        f = open(current_dir + "/search/class_individual.txt", 'w', encoding = 'utf8')
        for item in list_items:
            if "?" not in item:
                f.write(str(item) + '\n')
            else: pass
        print("done")
        f.close()

    elif 'find_food_by_calo' in sys.argv[1]:
        command = sys.argv[1]
        list_items = eval(command)
        f = open(current_dir + "/search/food_by_calo.txt", 'w', encoding = 'utf8')
        for item in list_items:
            if "?" not in item:
                f.write(str(item) + '\n')
            else: pass
        print("done")
        f.close()

    elif "food_calo" in sys.argv[1]:
        command = sys.argv[1]
        list_items = eval(command)
        f = open(current_dir + "/search/food_and_calo.txt", 'w', encoding = 'utf8')
        for item, value in list_items.items():
            if "?" not in item:
                f.write(str(item) + " " + str(value) + '\n')
            else: pass
        print("done")
        f.close()

    elif "testing" == sys.argv[1]:
        print(eval(sys.argv[2]))

    else:
        command = sys.argv[1]
        print(eval(command))

if __name__ == "__main__":
    try:
        main_query()
    except Exception as e:
        print("Your query maybe wrongs")
        print("Your mistake: ", e)
