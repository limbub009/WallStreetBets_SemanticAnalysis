import requests
import os
import json
import preprocessor as p #cleaner
from langdetect import detect #language detecter
from csv import writer #write to a csv file
import time



from ernie import SentenceClassifier
import numpy as np

bearer_token = "AAAAAAAAAAAAAAAAAAAAALb8bwEAAAAAhOXc%2BMLCqcc10LSNnFfHDl0rxfg%3D1rJZdgAHtuJEKIjSgBjVbwcuvtazWqd5C4WR6upslEilDgIfqS"
classifer = SentenceClassifier(model_path='WSBSemantic/utilfunc/modelSem')


output = {}

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

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
        headers = headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers,delete,bearer_token, input):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": input, "tag": input},
       # {"value": "cat has:images -grumpy", "tag": "cat pictures"},
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


def get_stream(headers, set, bearer_token):
    output = {}
    t_end = time.time() + 15
    print("time set")
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,  
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if time.time() > t_end:
            print("timeout")
            break
        if response_line:
            json_response = json.loads(response_line)
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            tweet = json_response['data']['text']
            tweet = p.clean(tweet)
            tweet = tweet.replace(":","")
            try:
                if detect(tweet) == 'en':
                    print(tweet)
                    try: #some tweets dont have text // not included
                        classes = ['Bearish', 'Neutral', 'Bullish']
                        probabilities = classifer.predict_one(tweet)
                        print(classes[np.argmax(probabilities)])
                        output[tweet] = classes[np.argmax(probabilities)]
                    except:
                        pass
            except:
                pass
    print("before break")
    return output

def main(x):
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token, x)
    output = get_stream(headers, set, bearer_token)
    print("ended")
    return output
    
    

if __name__ == "__main__":
    main()