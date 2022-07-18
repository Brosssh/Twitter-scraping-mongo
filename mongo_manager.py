from pymongo import MongoClient


def get_client():
    conn=""
    client=MongoClient(conn)
    return client

def insert_tweet(client, tweet_dict):
    print("\nStart pushing tweet in Mongo...")
    client.twitter.tweets.insert_one(tweet_dict)
    print("Tweet inserted in Mongo")

def insert_author(client, author_dict):
    print("\nStart pushing author in Mongo...")
    client.twitter.authors.insert_one(author_dict)
    print("Author inserted in Mongo")
