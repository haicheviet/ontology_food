from query_rdfs import check_individual_exist
import json
import sys
import os
from time import localtime, strftime

sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
current_dir = os.path.dirname("__file__")
current_dir = current_dir if current_dir is not '' else '.'
# directory to scan for any txt files
data_dir_path = current_dir + '/dev_insert'


#
# ─── INSERT DATA ────────────────────────────────────────────────────────────────
#

def insert_individual_food(
        Name_of_food, Type_food, Has_calo, Has_Nutrient,
        Has_suitable_time, Has_receipt, Not_Use_Together, root_file):

    line_to_replace = -41
    list_line_nutrient = len(Has_Nutrient)
    list_line_food_not_use = len(Not_Use_Together)

    if check_individual_exist(Name_of_food):
        with open(root_file, 'r', encoding="utf8") as file:
            lines = file.readlines()

        template = """
        <!-- http://www.co-ode.org/ontologies/ont.owl#{} -->

        <NamedIndividual rdf:about="&ont;{}">
            <rdf:type rdf:resource="&ont;{}"/>
            <ont:Has_calo rdf:datatype="&xsd;int">{}</ont:Has_calo>
            <ont:Has_processing rdf:datatype="&xsd;string">{}</ont:Has_processing>
            <ont:Has_suitable_time rdf:datatype="&xsd;string">{}</ont:Has_suitable_time>
        </NamedIndividual>
            \n\n\n""".format(Name_of_food, Name_of_food, Type_food, Has_calo, Has_receipt, Has_suitable_time)
        for count in range(list_line_nutrient):
            line_nutrient = '\t<ont:Has_Nutrient rdf:resource="&ont;{}"/>\n\t'.format(
                Has_Nutrient[count])
            index = template.find('</NamedIndividual>')
            template = template[:index] + line_nutrient + template[index:]

        for count in range(list_line_food_not_use):
            line_nutrient = '\t<ont:Not_Use_Together rdf:resource="&ont;{}"/>\n\t'.format(
                Not_Use_Together[count])
            index = template.find('</NamedIndividual>')
            template = template[:index] + line_nutrient + template[index:]

        if len(lines) > int(line_to_replace):
            lines[line_to_replace] = template

        with open(root_file, 'w', encoding="utf8") as file:
            file.writelines(lines)
        print("Done")
    else:
        print("Your food's already in database")

def insert_individual_nutrient(
        name, types, Has_exceed_effect,
        Has_lack_of_sb_effect, Has_effect, root_file):

    line_to_replace = -41

    if check_individual_exist(name):
        with open(root_file, 'r', encoding="utf8") as file:
            lines = file.readlines()

        template = """
    <!-- http://www.co-ode.org/ontologies/ont.owl#{} -->

    <NamedIndividual rdf:about="&ont;{}">
        <rdf:type rdf:resource="&ont;{}"/>
        <ont:Has_exceed_effect rdf:datatype="&xsd;string">{}</ont:Has_exceed_effect>
        <ont:Has_lack_of_sb_effect rdf:datatype="&xsd;string">{}</ont:Has_lack_of_sb_effect>
        <ont:Has_effect rdf:datatype="&xsd;string">{}</ont:Has_effect>
    </NamedIndividual>
            \n\n\n""".format(name, name, types, Has_exceed_effect, Has_lack_of_sb_effect, Has_effect)

        if len(lines) > int(line_to_replace):
            lines[line_to_replace] = template

        with open(root_file, 'w', encoding="utf8") as file:
            file.writelines(lines)
        print("Done")
    else:
        print("Your nutrient's already in database")


def insert_menu(date, input_menu, root_file):
    name = "Menu_" + str(date)
    template = """
     <!-- http://www.co-ode.org/ontologies/ont.owl#{} -->

    <NamedIndividual rdf:about="&ont;{}">
        <rdf:type rdf:resource="&ont;Menu"/>
        <ont:Has_Score rdf:datatype="&xsd;float">{}</ont:Has_Score>
        <ont:Has_Dinner_Menu rdf:datatype="&xsd;string">{}</ont:Has_Dinner_Menu>
        <ont:Has_name_user rdf:datatype="&xsd;string">{}</ont:Has_name_user>
        <ont:Has_Lunch_Menu rdf:datatype="&xsd;string">What up bro</ont:Has_Lunch_Menu>
        <ont:Has_Infomation rdf:datatype="&xsd;string">{}</ont:Has_Infomation>
        <ont:Has_Breakfast_Menu rdf:datatype="&xsd;string">{}</ont:Has_Breakfast_Menu>
    </NamedIndividual>
        \n\n\n""".format(name, name, input_menu['Score'],
                         input_menu['Dinner'], input_menu['Has_name'],
                         input_menu['Lunch'], input_menu['Has_information'],
                         input_menu['Breakfast'])
    line_to_replace = -41
    if check_individual_exist(name):
        with open(root_file, 'r', encoding="utf8") as file:
            lines = file.readlines()
        if len(lines) > int(line_to_replace):
            lines[line_to_replace] = template
        with open(root_file, 'w', encoding="utf8") as file:
            file.writelines(lines)
        print("Done")
    else:
        print("Your menu's already in database")
#
# ─── INPUT DATA AND CHECKING ────────────────────────────────────────────────────
#


if __name__ == "__main__":
    with open(data_dir_path + "/food.json", 'r', encoding='utf8') as food_data:
        food = json.load(food_data)
    with open(data_dir_path + "/nutrient.json", 'r', encoding='utf8') as nutrient_data:
        nutrient = json.load(nutrient_data)
    with open(data_dir_path + "/menu_pick.json", 'r', encoding='utf8') as menu_data:
        menu = json.load(menu_data)
    time = strftime("%m-%d.%H:%M", localtime())

    root_file = current_dir + "/data_raw/rdf-copy.owl"
    if sys.argv[1] == 'food':
        insert_individual_food(
            food["name"], food['type'], food['calo'], food['Has_Nutrient'],
            food["Has_suitable_time"], food["Has_processing"], food['Not_use_together'], root_file
        )
    elif sys.argv[1] == 'nutrient':
        insert_individual_nutrient(
            nutrient["name"], nutrient['type'], nutrient['Has_exceed_effect'],
            nutrient['Has_lack_of_sb_effect'], nutrient["Has_effect"], root_file
        )
    elif sys.argv[1] == 'menu':
        insert_menu(time, menu, root_file)
