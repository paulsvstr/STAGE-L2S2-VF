# Connexion à Wikidata
import requests

def fetch_wikidata(params):
    url = 'https://www.wikidata.org/w/api.php'
    try:
        return requests.get(url, params=params)
    except:
        return 'There was and error'
    
import string

#FONCTION D'ANALYSE DU MOT LE PLUS COMMUN DANS LES 
#DESCRIPTIONS WIKIDATA DES DIFFERENTS MOTS

def pt_commun(colonne) :
  dict = {}
  sgn_mots = [] #liste contenant des paires // ex : ['Lyon', 'ville de France']
  for mot in colonne :
    Ltemp = []
    Ltemp.append(mot)
    query = mot
    params = {
          'action': 'wbsearchentities',
          'format': 'json',
          'search': query,
          'language': 'en' }
    data = fetch_wikidata(params)
    data = data.json()
    data
    sgn = data['search'][0]['description']
    Ltemp.append(sgn)
    sgn_mots.append(Ltemp)
  for paire in sgn_mots :
    phrase = paire[1].split()
    for mot in phrase :
      mp = "".join([i for i in mot if i not in string.punctuation])
      mp = mp.lower()
      if mp not in dict :
        dict[mp] =1
      else :
        dict[mp] +=1
  max = 0
  L_max = []
  for keys in dict.keys() :
    if keys not in ['in','of','a','the','as','born','name','family','and','by','that'] :
      if dict[keys] == max :
        L_max.append(keys)
      if dict[keys] > max :
        L_max = []
        L_max.append(keys)
        max = dict[keys]

  return(L_max)
  
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
  data.append(pt_commun(liste[1:]))
end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.2}s')