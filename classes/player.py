from aiogram.types import User

from classes.role import Role


class Player:
    instances = []
    def __init__(self, user: User, game_id: int):
        self.id = user.id
        self.game_id = game_id
        self.name = user.full_name
        self.role: Role = Role()
        self.is_alive = True
        Player.instances.append(self)

    def __dict__(self) -> dict:
        return {"id": self.id,
                "role": self.role.id,
                "is_alive": self.is_alive}

    @classmethod
    def get(cls, player_id: int, game_id: int):
        return [inst for inst in cls.instances if inst.id == player_id and inst.game_id == game_id][0]
