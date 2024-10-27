from enum import Enum
import json

from aiogram import Bot
from aiogram.types import CallbackQuery, Message

from classes.player import Player
from classes.vote import Vote, NightVote, DayVote
from data.roles import mafia, lawyer, don
from database.database import is_user_in_db
from utils.logger import log_to_admins, notify_new_game


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
        self.win: str | None = None
        self.original_players = self.players

        Game.instances.append(self)

    async def appoint_admin(self, admin: Player):
        self.admin: Player = admin
        await self.add_player(admin)

    async def start(self):
        self.original_players = self.players
        self.state = GameState.night
        # self.dump_session()
        if self._notify_message is not None:
            await self._bot.delete_message(self._chat_id, self._notify_message.message_id)


    async def add_player(self, player: Player, callback: CallbackQuery | None = None) -> bool:
        if any([pl.id == player.id for pl in self.players]):
            return False
        if not is_user_in_db(player.id):
            if self._notify_message is None and callback is not None:
                self._notify_message = await callback.message.answer("<i>⚠️ Для участия в игре необходимо "
                                                                     "<a href='https://t.me/DonCorlBot?start=0'>"
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

    @staticmethod
    def kill_player(player: Player):
        player.is_alive = False


    def create_night_vote(self) -> Vote:
        new_vote = NightVote(self)
        self._votes.append(new_vote)
        return new_vote

    def create_day_vote(self) -> Vote:
        new_vote = DayVote(self)
        self._votes.append(new_vote)
        return new_vote

    def get_prev_night_vote(self, num: int) -> NightVote | None:
        ctr = 0
        for vote in self._votes[::-1]:
            if isinstance(vote, NightVote):
                ctr += 1
                if ctr == num:
                    return vote
        return None

    def get_prev_day_vote(self, num: int) -> DayVote | None:
        ctr = 0
        for vote in self._votes[::-1]:
            if isinstance(vote, DayVote):
                ctr += 1
                if ctr == num:
                    return vote
        return None


    async def goto_morning(self, callback: CallbackQuery):
        vote = self.get_prev_night_vote(1)
        killed_people = await vote.night_analyse()
        self.state = GameState.day
        for player in killed_people:
            player.is_alive = False
        if len(killed_people) != 0:
            await callback.message.answer(f'Город просыпается.\nК сожалению этой ночью были убиты: \n{", ".join([f"{victim.name}" for victim in killed_people])}')
        else:
            await callback.message.answer(f'Город просыпается.\nУдивительно, но все остались живы')

    async def goto_night(self, callback: CallbackQuery):
        vote = self.get_prev_day_vote(1)
        killed_people = await vote.day_analyse()
        self.state = GameState.night
        if killed_people is not None:
            killed_people.is_alive = False

            await callback.message.answer(f'{killed_people.name} был убит жителями города.')

    def mafia_team_count(self) -> int:
        count = 0
        for player in self.players:
            if player.role in [don, mafia, lawyer] and player.is_alive:
                count += 1
        return count

    def civilian_team_count(self) -> int:
        count = 0
        for player in self.players:
            if player.role not in [don, mafia, lawyer] and player.is_alive:
                count += 1
        return count

    async def mafia_win(self, callback: CallbackQuery):
        self.win = "mafia"
        self.state = GameState.ended
        await callback.message.answer(f"Мафия победила!\n\nУчастники команды мафии: {', '.join([f'{player.name}' for player in self.players if player.role in [mafia, don, lawyer]])}")
        self.instances.remove(self)

    async def civilian_win(self, callback: CallbackQuery):
        self.win = "civilian"
        self.state = GameState.ended
        await callback.message.answer(f"Мирные жители выиграли!\n\nУчастники команды мафии: {', '.join([f'{player.name}' for player in self.players if player.role in [mafia, don, lawyer]])}")
        self.instances.remove(self)



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
        try:
            return [inst for inst in cls.instances if inst.id == inst_id][0]
        except IndexError:
            return None


class GameState(Enum):
    waiting = "Waiting"
    night = "Night"
    day = "Day"
    ended = "Ended"
