from telethon import TelegramClient
from telethon import functions
import asyncio
import requests
import os
import json


# Remember to use your own values from my.telegram.org!
#DINGDONG
api_id = 8417724
api_hash = '19624df5fab9d43a0d5b9bf274e4f40d'
client = TelegramClient('anon', api_id, api_hash)
client.start()
loop = asyncio.get_event_loop()

async def searchTelegram():

    return await client(functions.contacts.SearchRequest(
        q="PancakeExpress Devs",
        limit=100
    ))

results = loop.run_until_complete(searchTelegram())

async def getEntity():
    return await client.get_entity(703925777)

ent = loop.run_until_complete(getEntity())

async def sendMessage(message):
    await client.send_message(entity=ent, message=message)

bearer_token = "AAAAAAAAAAAAAAAAAAAAABvkYwEAAAAAxyVasJKLRHo4063UC8oNqfFPkBI%3DhEdGUtje2nsSFA1RPW9B6m1GTy6f8nPyk0wbZxn4oq3D0ntE3W"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "from:elonmusk -is:quote -is:reply -is:retweet"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            message = "https://twitter.com/elonmusk/status/" + json_response['data']['id']
            loop.run_until_complete(sendMessage(message))


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    main()
