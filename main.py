import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap, ListedColormap
import nltk
from nltk.corpus import wordnet
from pymongo import MongoClient
import pymongo
import dns

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')




def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://noman4545:nomi75000@cluster0.ijlrj9y.mongodb.net/SPL_DB"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['SPL_DB']

def add_feature():
  feature1 = []
  while True:
    choice = input("if you want to continue press 1: ")
    if choice == "1":
      feature = input("Enter element name: ") 
      if feature in nouns:
        if feature in feature1:
          print("already available")
        else:    
          feature1.append(feature)
      else:
        print("element-name is not belong to the list")
    else:
      break 
  return feature1     

try:
    db = get_database()
except: 
    print("Error: mongodb not connected")   

data = db["noman-data"]    

#enter paragraph
paragraph = input("Enter paragraph")
#get noun from paragraph
is_noun = lambda pos: pos[:2] == 'NN'
tokenized = nltk.word_tokenize(paragraph)
nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
nouns = [var for var in nouns if len(var) > 1]
nouns = list(dict.fromkeys(nouns))
print(f"List of Unique Nouns from Paragarph: \n{nouns}")

# remove the simillar nouns by comparing with wordNet
length_nouns = len(nouns)
try:
  for i in range(length_nouns-1):
    increment = i + 1
    try:
        w1 = wordnet.synset(f'{nouns[i]}.n.01')
        w2 = wordnet.synset(f'{nouns[increment]}.n.01') # n denotes noun
        print(w1.wup_similarity(w2))
        score = w1.wup_similarity(w2)
        if score > 0.60:
          nouns.remove(nouns[increment])
    except:
      pass 
except IndexError:
  pass     
print(f"After removing the simillar nouns by comparing with wordNet  : \n{nouns}")  

first_choice = input("Enter 1 for Adding Feature &\nEnter 2 for comparing Features")

if first_choice == '1':
    feature_dic = {}
    while True:
        choice = input("if you to make feature press 1: ")
        if choice == "1":
            feature1 = input("Enter Feature Name: ")
            feature_dic[feature1] = add_feature()
        else:
            break
    data.insert_many([feature_dic])  
#compare the nouns with existing features  
elif first_choice == '2':
    for compare_element in nouns:
        opt_dic = {}
        results = {}
        for i in data.find():
            for key,value in i.items():
                if key != "_id":
                    all_scores = []
                    for element in value:
                      try:
                        w1 = wordnet.synset(f'{element}.n.01')
                        w2 = wordnet.synset(f'{compare_element}.n.01') # n denotes noun
                        print(w1.wup_similarity(w2))
                        score = w1.wup_similarity(w2)
                        all_scores.append(score)
                      except:
                        pass
                    mean_score = sum(all_scores)/len(all_scores)
                    opt_dic = {
                    str(key): mean_score
                    }
                    results.update(opt_dic)
        max_key_result = max(results, key=results.get)
        print(max_key_result)

        names = list(results.keys())
        values = list(results.values())
        values_color=list(map(lambda names: 'green' if names == max_key_result else 'skyblue', names))
        plt.bar(range(len(results)), values, tick_label=names,color= values_color)
        plt.title(str(compare_element))
        
        plt.show()


