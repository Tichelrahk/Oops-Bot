import sys

#From framework
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit

#From project
from game_player import GamePlayer


class Enemy(GamePlayer):
    def __init__(self):
        super().__init__()
        self.has_homebase_base = True

    def has_base(self):
        return self.has_homebase_base