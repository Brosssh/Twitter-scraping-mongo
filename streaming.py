import requests
import json
import mongo_manager
import scraping

data = []
MongoClient=mongo_manager.get_client()
counter = 0

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    sample_rules = [
        {"value": "#samsung lang:en", "tag": "samsung"},
        {"value": "#apple lang:en", "tag": "apple"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token, MongoClient):
    global data, counter
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    print(response.status_code)
    print("Starting fetching datas")
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            id=json_response["data"]["id"]
            print("Detected a message with ID", id)
            cleaned=scraping.get_json_twitter(id)
            print("Tweet cleaned!")
            if "author_name" in cleaned:
                user=scraping.get_json_author(str(cleaned["author_name"]))
                print("User cleaned!")
                user["author_name"]=cleaned.pop("author_name")
                user["author_alias"] = cleaned.pop("author_alias")
                cleaned["author"]=user
                mongo_manager.insert_tweet(MongoClient,cleaned)
                print("\n\n\n")
            json.dumps(json_response, indent=4, sort_keys=True)
            data.append(json_response['data'])

def start_streaming():
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAADBkYAEAAAAApAv29RWuU9J5ayq0w4CD7PUpv6A%3DIR1fH7suWwsnLhEnQkwWJI7yaYjkiA1iEmMNWX1BMk1yodTDw2'
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token, MongoClient)
