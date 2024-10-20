from aiogram.types import FSInputFile
from dataclasses import dataclass


@dataclass
class Role:
    id: id = -1
    name: str = ""
    description: str = ""
    photo: FSInputFile = None
