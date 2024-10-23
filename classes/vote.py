from classes.game import Game
from classes.player import Player


class Vote:
    def __init__(self, game: Game) -> None:
        self._game = game


class NightVote(Vote):
    active_roles: list[int] = [0, 2, 3, 4, 5, 6, 7, 8]
    type = 'Night'

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.mafia_votes: list[Player] = []
        self.don_check: Player | None = None
        self.sheriff_check: Player | None = None
        self.lawyer_def: Player | None = None
        self.doctor_def: Player | None = None
        self.prostitute_sleep: Player | None = None
        self.maniac_victim: Player | None = None

    def get_votes_count(self) -> int:
        count = 0
        for player in self._game.players:
            if player.role.id in self.active_roles:
                if player.role.id == 8: # SERGEANT
                    sheriffs = [i for i in self._game.players if i.role.id == 4 and i.is_alive]
                    if len(sheriffs) != 0:
                        continue
            count += 1
        return count

    def mafia_vote(self, victim: Player) -> None:
        self.mafia_votes.append(victim)

    def don_check(self, target: Player) -> None:
        self.don_check = target

    def sheriff_check(self, target: Player) -> None:
        self.sheriff_check = target

    def lawyer_def(self, target: Player) -> None:
        self.lawyer_def = target

    def doctor_def(self, target: Player) -> None:
        self.doctor_def = target

    def prostitute_sleep(self, target: Player) -> None:
        self.prostitute_sleep = target

    def maniac_victim(self, target: Player) -> None:
        self.maniac_victim = target

    def __dict__(self):
        return {
            "type": self.type,
            "mafia_votes": [vote.name for vote in self.mafia_votes],
            "don_check": self.don_check,
            "sheriff_check": self.sheriff_check,
            "lawyer_def": self.lawyer_def,
            "doctor_def": self.doctor_def,
            "prostitute_sleep": self.prostitute_sleep,
            "maniac_victim": self.maniac_victim
        }