from aiogram.types import User

from classes.role_class import Role


class Member:
    instances = []
    def __init__(self, data: User):
        self.id = data.id
        self.name = data.full_name
        self.role: Role = Role()
        self.is_alive = True #  TODO
        Member.instances.append(self)

    def __dict__(self):
        return {"id": self.id,
                "role": self.role.id,
                "is_alive": self.is_alive}

    @classmethod
    def get_by_id(cls, inst_id: int):
        return [inst for inst in cls.instances if inst.id == inst_id][0]
