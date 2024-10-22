from aiogram.types import FSInputFile
from dataclasses import dataclass


@dataclass
class Role:
    id: id = -1
    name: str = ""
    description: str = ""
    photo: FSInputFile = None

    def format_message(self):
        return (f"<b>{self.name}</b>\n\n"
                f"{self.description}")
