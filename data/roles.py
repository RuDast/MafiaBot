from classes.role_class import Role
import json

with open("data/roles.json", encoding="utf-8") as file:
    roles_data = json.load(file)

mafia = Role(id=roles_data["mafia"]["id"],
             name=roles_data["mafia"]["name"],
             description=roles_data["mafia"]["description"])

civilian = Role(id=roles_data["civilian"]["id"],
                name=roles_data["civilian"]["name"],
                description=roles_data["civilian"]["description"])

sheriff = Role(id=roles_data["sheriff"]["id"],
               name=roles_data["sheriff"]["name"],
               description=roles_data["sheriff"]["description"])

roles_list = [civilian, civilian, civilian, mafia, sheriff]
