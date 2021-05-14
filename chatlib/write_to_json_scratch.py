import json

users = {
    "omri": {
        "password": "1234",
        "score": 0,
        "questions_asked": []

    }
}
#### Write to json file ####
with open("C:\\Users\\OMRI\\PycharmProjects\\networksPy\\chatlib\\users.json", 'w') as f:
    json.dump(users, f)

if "omri" in users.keys():
    print("HI")
