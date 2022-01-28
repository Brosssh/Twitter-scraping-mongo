import json

import mongo_manager

def to_lower_dict(mydict):
    list_lowered = []
    list_count = []
    for el in mydict:
        if str(el).lower() in list_lowered:
            list_count[list_lowered.index(str(el).lower())] += mydict[el]
        else:
            list_lowered.append(str(el).lower())
            list_count.append(int(mydict[el]))
    return dict(zip(list_lowered,list_count))

def count_hashtags():
    query=[{"$unwind": "$hashtags"},{"$group": {"_id": { "hashtags" : "$hashtags"},"count": {"$sum": 1}}}]
    client=mongo_manager.get_client()
    lista=list(client.twitter.tweets.aggregate(query))
    dict_hashtags={}
    for el in lista:
        dict_hashtags[el["_id"]["hashtags"]]=el["count"]

    dict_hashtags=to_lower_dict(dict_hashtags)
    return dict_hashtags


def count_impact_hashtags():
    client = mongo_manager.get_client()
    lista = list(client.twitter.tweets.find({"$and":[{"hashtags": {"$exists":1}},{"author.followers":{"$exists":1}}]},{"hashtags":1,"author.followers":1,"_id":0}))
    dict_hashtags={}
    for el in lista:
        el=dict(el)
        for name in el["hashtags"]:
            numero=str(el["author"]["followers"])
            if "," in str(numero):
                numero = numero.replace(",", "")
            if numero[-1] == "K" and "." in numero:
                numero = int(numero[:-1].replace(".", "")) * 100
            elif numero[-1] == "M" and "." in numero:
                numero = int(numero[:-1].replace(".", "")) * 100000
            elif numero[-1] == "K" and "." not in numero:
                numero = int(numero[:-1].replace(".", "")) * 1000
            elif numero[-1] == "M" and "." not in numero:
                numero = int(numero[:-1].replace(".", "")) * 1000000
            if str(name).lower() in dict_hashtags.keys():
                dict_hashtags[str(name).lower()]+=int(numero)
            else:
                dict_hashtags[str(name).lower()]=int(numero)
    return dict_hashtags

def tweets_for_author():
    query = [{"$group": {"_id": {"autore": "$author.author_name"}, "count": {"$sum": 1}}}]
    client = mongo_manager.get_client()
    lista = list(client.twitter.tweets.aggregate(query))
    mydict = {}
    for el in lista:
        mydict[el["_id"]["autore"]] = el["count"]
    return mydict

def apple_on_android():
    client = mongo_manager.get_client()
    lista = list(client.twitter.tweets.find(
        {"$and": [{"hashtags": {"$regex": '[Aa][Pp]{2}[Ll][Ee]'}}, {"source": "Twitter for Android"}]}))
    lista2 = list(client.twitter.tweets.find(
        {"$and": [{"hashtags": {"$regex": '[Ss][Aa][Mm][Ss][Uu][Nn][Gg]'}}, {"source": "Twitter for iPhone"}]}))
    return {"apple_on_android":len(lista),"samsung_on_apple":len(lista2)}

def impact_for_user():
    client = mongo_manager.get_client()
    lista = list(client.twitter.tweets.find({"$and":[{"author.author_name": {"$exists":1}},{"author.followers":{"$exists":1}}]},{"author.author_name":1,"author.followers":1,"_id":0}))
    mydict={}
    for el in lista:
        numero = str(el["author"]["followers"])
        if "," in str(numero):
            numero = numero.replace(",", "")
        if numero[-1] == "K" and "." in numero:
            numero = int(numero[:-1].replace(".", "")) * 100
        elif numero[-1] == "M" and "." in numero:
            numero = int(numero[:-1].replace(".", "")) * 100000
        elif numero[-1] == "K" and "." not in numero:
            numero = int(numero[:-1].replace(".", "")) * 1000
        elif numero[-1] == "M" and "." not in numero:
            numero = int(numero[:-1].replace(".", "")) * 1000000
        mydict[el["author"]["author_name"]] = int(numero)
        #mydict[el["author"]["author_name"]] = el["author"]["followers"]
    return mydict

def hashtags_tweets_for_author():
    client = mongo_manager.get_client()
    lista = list(client.twitter.tweets.find(
        {"$and": [{"author.author_name": {"$exists": 1}}, {"hashtags": {"$exists": 1}}]},
        {"author.author_name": 1, "hashtags": 1}))
    mydict={}
    for el in lista:
        if el["author"]["author_name"] in mydict:
            mydict[el["author"]["author_name"]]+=el["hashtags"]
        else:
            mydict[el["author"]["author_name"]]=el["hashtags"]
    return mydict

with open("./output_files/tweets_for_author.json", "w") as outfile:
    json.dump(tweets_for_author(), outfile)

print("tweets_for_author json created")

with open("./output_files/count_impact_hashtags.json", "w") as outfile:
    json.dump(count_impact_hashtags(), outfile)

print("count_impact_hashtags json created")

with open("./output_files/count_hashtags.json", "w") as outfile:
    json.dump(count_hashtags(), outfile)

print("count_hashtags json created")

with open("./output_files/apple_on_android.json", "w") as outfile:
    json.dump(apple_on_android(), outfile)

print("apple_on_android json created")

with open("./output_files/impact_for_user.json", "w") as outfile:
    json.dump(impact_for_user(), outfile)

print("impact_for_user json created")

with open("./output_files/hashtags_tweets_for_author.json", "w") as outfile:
    json.dump(hashtags_tweets_for_author(), outfile)

print("hashtags_tweets_for_author json created")
