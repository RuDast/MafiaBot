from asyncio import sleep

from aiogram.types import CallbackQuery

from classes.player import Player
from data.config import config
from data.roles import prostitute


class Vote:
    def __init__(self, game) -> None:
        self._game = game


class NightVote(Vote):
    active_roles: list[int] = [0, 2, 3, 4, 5, 6, 7, 8]
    type = 'Night'

    def __init__(self, game) -> None:
        super().__init__(game)
        self.mafia_votes: dict[str: Player] = {}
        self.don_check: Player | None = None
        self.sheriff_check: Player | None = None
        self.lawyer_def: Player | None = None
        self.doctor_heal: Player | None = None
        self.prostitute_sleep: Player | None = None
        self.maniac_victim: Player | None = None

    def get_max_votes_count(self) -> int:
        count = 0
        for player in self._game.players:
            if not player.is_alive:
                continue

            if player.role.id in self.active_roles:
                if player.role.id == 8: # SERGEANT
                    sheriffs = [i for i in self._game.players if i.role.id == 4 and i.is_alive]
                    if len(sheriffs) != 0:
                        continue
            count += 1
        return count

    def get_votes_count(self) -> int:
        count = 0
        for player in self._game.players:
            if player.role.id == 0:
                pass
        # TODO доделать
        return count

    def mafia_vote(self, mafia: Player, victim: Player) -> None:
        if str(mafia.id) not in self.mafia_votes.keys():
            self.mafia_votes[str(mafia.id)] = victim

    def get_killed_player(self) -> Player | None:
        killed_players: list[Player] = []
        for value in self.mafia_votes.values():
            killed_players.append(value)
        if len(killed_players) == 0:
            return None
        return max(killed_players, key=killed_players.count)

    async def night_analyse(self) -> list[Player]:
        await sleep(config["NIGHT_TIME"])

        killed_players = []

        mafia_victim = self.get_killed_player()
        if self.doctor_heal != mafia_victim and self.prostitute_sleep != mafia_victim:
            self._game.kill_player(mafia_victim)
            killed_players.append(mafia_victim)

            if mafia_victim.role == prostitute:
                if self.prostitute_sleep is not None:
                    self._game.kill_player(self.prostitute_sleep)
                    killed_players.append(self.prostitute_sleep)
        return killed_players




