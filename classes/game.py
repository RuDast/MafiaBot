from enum import Enum
import json

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from classes.player import Player
from classes.vote import Vote, NightVote
from database.database import is_user_in_db


class Game:
    instances = []

    def __init__(self, bot: Bot, chat_id: int) -> None:
        with open("database/database.json", encoding="utf-8", mode="r") as file:
            self.id = int(json.load(file)["last_game_id"]) + 1
        with open("database/database.json", encoding="utf-8", mode="w") as file:
            json.dump({"last_game_id": self.id}, file)
        self.state: GameState = GameState.waiting
        self.admin: Player | None = None
        self.players: list[Player] = []
        self._votes: list[Vote] = []
        self._bot = bot
        self._chat_id = chat_id
        self._notify_message: Message | None = None
        Game.instances.append(self)

    async def appoint_admin(self, admin: Player):
        self.admin: Player = admin
        await self.add_player(admin)

    async def start(self):
        self.state = GameState.night
        self.dump_session()
        if self._notify_message is not None:
            await self._bot.delete_message(self._chat_id, self._notify_message.message_id)

    async def add_player(self, player: Player, callback: CallbackQuery | None = None) -> bool:
        if any([pl.id == player.id for pl in self.players]):
            return False
        if not is_user_in_db(player.id):
            if self._notify_message is None and callback is not None:
                self._notify_message = await callback.message.answer("<i>⚠️ Для участия в игре необходимо "
                                                                     "<a href='https://t.me/testfloppa13bot?start=0'>"
                                                                     "написать боту</a>.</i>")

            return False

        self.players.append(player)
        return True

    def remove_player(self, player: Player) -> bool:
        for pl in self.players:
            if pl.id == player.id:
                self.players.remove(pl)
                return True
        return False

    def create_night_vote(self) -> Vote:
        self._votes.append(NightVote(self))
        return self._votes[-1]

    def get_last_vote(self) -> Vote:
        return self._votes[-1]

    def dump_session(self):
        with open(f"database/sessions/session_{self.id}.json", encoding="utf-8", mode="w") as file:
            json.dump(self.__dict__(), file)

    def __dict__(self):
        return {
            "id": self.id,
            "state": self.state.value,
            "admin": self.admin.id,
            "players": [player.__dict__() for player in self.players],
            "votes": [vote.__dict__ for vote in self._votes]
        }

    @classmethod
    def find_by_id(cls, inst_id: int):
        return [inst for inst in cls.instances if inst.id == inst_id][0]


class GameState(Enum):
    waiting = "Waiting"
    night = "Night"
    day = "Day"
    ended = "Ended"
