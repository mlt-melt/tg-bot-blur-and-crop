import json

def update(dictionary):
    with open("data/data.txt", "w") as f:
        text = json.dumps(dictionary)
        f.write(text)

def check(user_id):
    with open("data/data.txt", "r") as f:
        text = f.read()
        usersData = json.loads(text)
    return usersData[str(user_id)]

def change_mode(user_id, mode):
    with open("data/data.txt", "r") as f:
        text = f.read()
        usersData = json.loads(text)
    usersData[str(user_id)] = mode
    update(usersData)