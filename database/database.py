import json


def add_new_member(member_id):
    with open("database/users.json") as file:
        templates = json.load(file)["users"]
    if member_id not in templates:
        templates.append(member_id)
        with open("database/users.json", encoding="utf-8", mode="w") as file:
            json.dump({"users": templates}, file)


def check_members():
    with open("database/users.json") as file:
        templates = json.load(file)["users"]
    return templates
