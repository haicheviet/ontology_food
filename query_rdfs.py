# -*- coding: utf-8 -*-
from owlready2 import *

class SparqlQueries:
    def __init__(self):
        my_world = World()
        my_world.get_ontology("file://D:/ontology_food/rdf.owl").load() #path to the owl file is given here
        sync_reasoner(my_world)  #reasoner is started and synchronized here
        self.graph = my_world.as_rdflib_graph()

    def search(self):
        #Search query is given here
        #Base URL of your ontology has to be given here
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

        #query is being run
        resultsList = self.graph.query(query)

#         creating json object
        response = []
        for item in resultsList:
            s = str(item['s'].toPython())
            s = re.sub(r'.*#',"",s)

            p = str(item['p'].toPython())
            p = re.sub(r'.*#', "", p)

            o = str(item['o'].toPython())
            o = re.sub(r'.*#', "", o)
            response.append({'label' : s, 'p' : p, "o" : o})
#             response.append({'label' : s})

        print(response) #just to show the output
        return response
if __name__ == "__main__":
    query = SparqlQueries()
    result = query.search()
    
