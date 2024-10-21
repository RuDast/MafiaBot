from enum import Enum
import json

from classes.member_class import Member
from database.database import is_member_in_db


class Game:
    instances = []
    def __init__(self, admin: Member) -> None:
        with open("database/database.json", encoding="utf-8", mode="r") as file:
            self.id = int(json.load(file)["last_game_id"]) + 1
        with open("database/database.json", encoding="utf-8", mode="w") as file:
            json.dump({"last_game_id": self.id}, file)
        self.state: GameState = GameState.waiting
        self.admin: Member = admin
        self.players_count: int = 1
        self.players: list[Member] = [admin]
        Game.instances.append(self)

    def add_member(self, member: Member) -> bool:
        if any([member.id == player.id for player in self.players]) or not is_member_in_db(member.id):
            return False
        self.players.append(member)
        self.players_count += 1
        return True

    def delete_member(self, member: Member) -> bool:
        for player in self.players:
            if player.id == member.id:
                self.players.remove(player)
                return True
        return False

    def __str__(self):
        return (f'Game ID: {self.id}\n'
                f'Game State: {self.state.value}\n'
                f'---\n'
                f'Admin: {self.admin.name} #{self.admin.id}\n'
                f'Players:'
                f'\n')+ '\n'.join(f'{player.name} #{player.id} - {player.role.name}'  for player in self.players)

    def __dict__(self):
        return {"id": self.id,
                "state": self.state.value,
                "admin": self.admin.id,
                "players_count": self.players_count,
                "players": [player.__dict__() for player in self.players]}

    @classmethod
    def get_by_id(cls, inst_id: int):
        return [inst for inst in cls.instances if inst.id == inst_id][0]



class GameState(Enum):
    waiting = "Waiting"
    started = "Started"
    ended = "Ended"
