import sys


#From framework
from sc2.position import Point2
from sc2.bot_ai import BotAI


class GamePlayer(BotAI):
    #properties

    async def on_start(self):
        townhalls = self.townhalls()
        base_locations = []
        for t in townhalls:
            base_locations.append(t.position)
        army_locations = {}
        setattr(self, "base_locations", base_locations)
        setattr(self, "army_locations", army_locations)


    def has_base(self):
        if len(self.base_locations) > 0:
            return True
        else:
            return False