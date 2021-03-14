import json

with open("tests\Success_API_responses\dct.json", "r") as f:
    # data = json.loads(f.read())/
    data = json.load(f)
    print(data)
