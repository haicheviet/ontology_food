# -*- coding: utf-8 -*-
from owlready2 import *
import sys
import os
import json


class SparqlQueries:
    def __init__(self, data_dir_path):
        my_world = World()
        # path to the owl file is given here
        my_world.get_ontology("file://%s" % data_dir_path).load()
        sync_reasoner(my_world)  # reasoner is started and synchronized here
        self.graph = my_world.as_rdflib_graph()

    def search(self):
        # Search query is given here
        # Base URL of your ontology has to be given here
        query = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> " \
                "PREFIX FoodKB: <http://websemantic.net/2013/FoodKB#>"\
                "SELECT ?s ?p ?o " \
                "WHERE { " \
                "?s ?p ?o . " \
                "}"

#         query = """
#                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#                 PREFIX FoodKB: <http://websemantic.net/2013/FoodKB#>
#                 SELECT ?label
#                 WHERE { <http://websemantic.net/2013/FoodKB#Has_Activity_Level> rdfs:label ?label} }
#             """

        resultsList = self.graph.query(query)

#         creating json object
        response = []
        for item in resultsList:
            s = str(item['s'].toPython())
            s = re.sub(r'.*#', "", s)

            p = str(item['p'].toPython())
            p = re.sub(r'.*#', "", p)

            o = str(item['o'].toPython())
            o = re.sub(r'.*#', "", o)
            response.append({'label': s, 'p': p, "o": o})
#             response.append({'label' : s})

        # print(response)  # just to show the output
        return response


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname("__file__"), '..'))
    current_dir = os.path.dirname("__file__")
    current_dir = current_dir if current_dir is not '' else '.'
    # directory to scan for any owl files
    try:
        data_dir_path = current_dir + '/data_raw/{}'.format(sys.argv[1])
        print(sys.argv[1])
    except:
        data_dir_path = current_dir + '/data_raw/rdf.owl'

    query = SparqlQueries(data_dir_path)
    clean_data = query.search()
    with open(current_dir + "/data_after_clean/result_after_clean.json", 'w')as f:
        f.write(json.dumps(clean_data))
