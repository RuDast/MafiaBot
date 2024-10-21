import json

from aiogram.types import FSInputFile

from classes.role_class import Role

with open("roles.json", encoding="utf-8") as file:
    roles_data = json.load(file)

civilian = Role(id=roles_data["civilian"]["id"],

                name=roles_data["civilian"]["name"],
                description=roles_data["civilian"]["description"],
                photo=FSInputFile(roles_data["civilian"]["photo"]))

mafia = Role(id=roles_data["mafia"]["id"],

             name=roles_data["mafia"]["name"],
             description=roles_data["mafia"]["description"],
             photo=FSInputFile(roles_data["mafia"]["photo"]))

sheriff = Role(id=roles_data["sheriff"]["id"],
               name=roles_data["sheriff"]["name"],
               description=roles_data["sheriff"]["description"],
               photo=FSInputFile(roles_data["sheriff"]["photo"]))

prostitute = Role(id=roles_data["prostitute"]["id"],
                  name=roles_data["prostitute"]["name"],
                  description=roles_data["prostitute"]["description"],
                  photo=FSInputFile(roles_data["prostitute"]["photo"]))

don = Role(id=roles_data["don"]["id"],
           name=roles_data["don"]["name"],
           description=roles_data["don"]["description"],
           photo=FSInputFile(roles_data["don"]["photo"]))

lawyer = Role(id=roles_data["lawyer"]["id"],
              name=roles_data["lawyer"]["name"],
              description=roles_data["lawyer"]["description"],
              photo=FSInputFile(roles_data["lawyer"]["photo"]))

doctor = Role(id=roles_data["doctor"]["id"],
              name=roles_data["doctor"]["name"],
              description=roles_data["doctor"]["description"],
              photo=FSInputFile(roles_data["doctor"]["photo"]))

maniac = Role(id=roles_data["maniac"]["id"],
              name=roles_data["maniac"]["name"],
              description=roles_data["maniac"]["description"],
              photo=FSInputFile(roles_data["maniac"]["photo"]))

sergeant = Role(id=roles_data["sergeant"]["id"],
                name=roles_data["sergeant"]["name"],
                description=roles_data["sergeant"]["description"],
                photo=FSInputFile(roles_data["sergeant"]["photo"]))

kamikaze = Role(id=roles_data["kamikaze"]["id"],
                name=roles_data["kamikaze"]["name"],
                description=roles_data["kamikaze"]["description"],
                photo=FSInputFile(roles_data["kamikaze"]["photo"]))

roles_list = [civilian, civilian, civilian, mafia, sheriff, prostitute, mafia, civilian, doctor, maniac, civilian,
              mafia, civilian, don, civilian, mafia, sergeant, lawyer, civilian, mafia]
