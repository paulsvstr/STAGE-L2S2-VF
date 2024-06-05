from rdflib import Graph
from pandas import DataFrame
from rdflib.plugins.sparql.processor import SPARQLResult
from collections import Counter


def sparql_results_to_df(results: SPARQLResult) -> DataFrame:
    """
    Export results from an rdflib SPARQL query into a `pandas.DataFrame`,
    using Python types. See https://github.com/RDFLib/rdflib/issues/1179.
    """
    return DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in results),
        columns=[str(x) for x in results.vars],
    )

def trouver_type_mot(graph, mot):
    query = f"""
        SELECT DISTINCT ?X ?Y ?Z ?obj ?Class
        WHERE {{
            ?X rdfs:label "{mot}"@en.
            ?X rdf:type ?obj .
            ?obj rdfs:subClassOf* ?Class.
            OPTIONAL {{?Class rdfs:label ?Y filter (lang(?Y) = "en")}}.
            OPTIONAL {{?Class rdfs:label ?Z filter (lang(?Z) = "fr")}}.
        }}
    """
    # Exécuter la requête SPARQL
    retour = graph.query(query)
    resultsPD = sparql_results_to_df(retour)
    
    type_en,type_fr = [],[]
    for i in range(len(resultsPD['Y'])) :
        ten = resultsPD['Y'][i]
        tfr = resultsPD['Z'][i]
        if ten != None :
            type_en.append(ten)
        if tfr != None :
            type_fr.append(tfr)
    return type_en

graph = Graph("SPARQLStore")
graph.open("https://yago-knowledge.org/sparql/query")


def trouver_sens_liste(L) :
    context = []
    dict = {} 
    for mot in L :
        defi = []
        defi = trouver_type_mot(graph,mot)
        defi = list(set(defi))
        for item in defi :
            context.append(item)
    for terme in context :
        if terme not in dict :
            dict[terme] =1
        else :
            dict[terme] +=1
    max = 0
    L_max = []
    for keys in dict.keys() :
        if dict[keys] == max :
            L_max.append(keys)
        if dict[keys] > max :
            L_max = []
            L_max.append(keys)
            max = dict[keys]
    return L_max

##################################################################
#                                                                #
#                       EVALUATION                               #
#                                                                #
##################################################################
dataset = [
        ["ville", "Paris", "Lyon", "Marseille", "Londres", "Berlin", "Rome"],     
        ["pays", "France", "Allemagne", "Italie", "Espagne", "Royaume-Uni", "États-Unis"],
        ["Profession", "Doctor", "Teacher", "Police Officer", "Plumber", "Artist", "Engineer"],
        ["Day of the Week", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        ["Year", "2011", "2012", "2013", "2014", "2015", "2016"],
        ["Month of the Year", "January", "February", "March", "April", "May", "June"],
        ["Mathematical Operation", "Number", "Addition", "Subtraction", "Multiplication", "Division", "Equation"],
        ["Vehicle", "Car", "Motorcycle", "Bicycle", "Truck", "Airplane", "Boat"],
        ["Chemical Element", "Hydrogen", "Oxygen", "Carbon", "Nitrogen", "Iron", "Copper"],
        ['College','Cambridge','Oxford','Harvard','Stanford','Berkeley','Columbia'],
        ["intstrument",'piano','guitar','violin','saxophone','cello','flute'],
        ["Flower", "Rose", "Lily", "Daisy", "Tulip", "Orchid", "Sunflower"],
        ["Jewelry", "Ring", "Necklace", "Bracelet", "Earrings", "Watch", "Brooch"],
        ["School Subject", "Math", "Science", "History", "Geography", "English", "Art"],
        ["Weather", "Sunny", "Rainy", "Cloudy", "Snowy", "Windy", "Stormy"],
        ["Technology", "Computer", "Smartphone", "Tablet", "Smartwatch", "Printer", "Router"],
        ["Clothing", "Shirt", "Pants", "Dress", "Skirt", "Jacket", "Sweater"],
        ["Dessert", "Cake", "Ice Cream", "Pie", "Pudding", "Brownie", "Cookie"],
        ["Tool", "Hammer", "Screwdriver", "Wrench", "Pliers", "Saw", "Drill"],
        ["Bird", "Eagle", "Sparrow", "Parrot", "Owl", "Pigeon", "Crow"],
        ["Fish", "Salmon", "Tuna", "Trout", "Shark", "Goldfish", "Mackerel"],
        ["Book Genre", "Fiction", "Non-fiction", "Mystery", "Fantasy", "Biography", "Science Fiction"],
        ["Holiday", "Christmas", "Easter", "Thanksgiving", "Halloween", "New Year", "Valentine's Day"],
        ["Body Part", "Arm", "Leg", "Head", "Hand", "Foot", "Eye"],
        ["Emotion", "Happy", "Sad", "Angry", "Surprised", "Mad", "Scared"],
        ["Continent", "Africa", "Asia", "Europe", "North America", "South America", "Australia"],
        ]
import time
start = time.time()


data = []
for liste in dataset :
  print('ok')
  data.append(trouver_sens_liste(liste[1:]))
end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.2}s')

