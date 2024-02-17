import pickle
mein_dictionary = {6969: ["ip",1],6000: ["ip2",0],6001: ["ip3",0]}

with open("data.pickle", 'wb') as datei:
    pickle.dump(mein_dictionary, datei)