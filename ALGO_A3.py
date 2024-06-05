from math import sqrt
import numpy as np
from collections import Counter

from sklearn.neighbors import NearestNeighbors
import time
start = time.time()
def load_data() :
    vect = open('/home/psevestre/glove.6B.50d.txt','r')
    x = []
    y = []
    lines = vect.readlines()
    dico = {}
    cpt = 0
    for k in range(0,400000): #création d'un dictionnaire dico[mot] = coordonnées
        C,L,D,temp,temp_str = [],[],[],[],[]
        L=lines[k]
        D = L.replace("\n","")
        #V = D.replace(",","")
        C = D.split(" ")
        temp_str = C[1:]
        temp = [float(i) for i in temp_str]
        x.append(temp)
        y.append(C[0])
        cpt +=1
    X = np.array(x)
    Y = np.array(y)
    return X,Y

coord,mots = load_data()
print("OK")
end1 = time.time()
k=200
kpp = NearestNeighbors(n_neighbors=k, metric='cosine')
kpp.fit(coord)

def word_2_coord(mot) :
    for i in range(len(mots)) :
        if mots[i] == mot : 
            return coord[i]
    else :
        return 'erreur'

def find_word_knn(mot_entree) :
    coord = word_2_coord(mot_entree)
    C = []
    
    if str(coord) == 'erreur' :
        C.append(coord)
        return C
    
    C.append(coord)
    F = np.array(C)
    distances, indices = kpp.kneighbors(F)
    neighbor_labels = mots[indices.flatten()]
    #print(f"Les 100 plus proches voisins sont : {neighbor_labels}")
    return(neighbor_labels)

def find_sens(L) : #L une liste de mots en MINISCULE dont on veut savoir le sens commun
    V, all_neigh =[],[]
    L_lower = []
    for mot in L :
        L_lower.append(mot.lower())
    for m in L_lower :
        V = find_word_knn(m)
        for v in V :
            all_neigh.append(v)
    sorted_words = [word for word, count in Counter(all_neigh).most_common()]

    for item in sorted_words[0:100] :
        if item not in L_lower :
            print(f"Le sens commun de cette liste est probablement : {item}")
            return item
            break

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
  data.append(find_sens(liste[1:]))
end2 = time.time()
elapsed1 = end1 - start
elapsed2 = end2 - start

print(f'Temps d\'exécution total : {elapsed2:.2}s')
print(f'Temps de chargement des données : {elapsed1:.2}s')