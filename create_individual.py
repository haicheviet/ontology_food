from query_rdfs import check_individual_exist
import


#
# ─── INSERT DATA ────────────────────────────────────────────────────────────────
#


def insert_individual_food(
        Name_of_food, Type_food, Has_calo, Has_Nutrient,
        Has_suitable_time, Has_receipt, Not_Use_Together):
    my_file = "rdf - Copy.owl"
    line_to_replace = -21

    with open(my_file, 'r', encoding="utf8") as file:
        lines = file.readlines()

    template = """    
        <!-- http://www.co-ode.org/ontologies/ont.owl#{} -->

        <NamedIndividual rdf:about="&ont;{}">
            <rdf:type rdf:resource="&FoodKB;{}"/>
            <ont:has_calo rdf:datatype="&xsd;int">{}</ont:has_calo>
        </NamedIndividual>
        \n\n\n""".format(Name_of_food, Name_of_food, Type_food, Has_calo)

    if len(lines) > int(line_to_replace):
        lines[line_to_replace] = template

    with open(my_file, 'w', encoding="utf8") as file:
        file.writelines(lines)


def insert_individual_nutrients(
        Name_of_nutrients, Has_effect, Has_exceed_effect,


def insert_individual_custormer(
        Name_of_Cus, Has_id, Has_height,
        Has_lackof_effect, Has_needed_amount):
        Has_weight, Has_BMI_Level, Has_Activity_Level_Value
        Has_Menu=None):


def insert_individual_health(
        Name_of_object, Has_food_needed, Has_food_avoided,
        Has_food_not_much, Has_needed_amount):

    #
    # ─── INPUT DATA AND CHECKING ────────────────────────────────────────────────────
    #


def input_data():


if __name__ == "__main__":
    input = 
