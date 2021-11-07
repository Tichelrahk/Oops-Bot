import sys


#From framework
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units

#From project
from game_player import GamePlayer
from base_command import BaseCommand
from army_command import ArmyCommand
from early_game import EarlyGame
from late_game import LateGame
from enemy_player import Enemy



class OopsBot(BotAI, GamePlayer):
    def has_base(self):
        if self.townhalls.amount > 0:
            return True
        else:
            return False

    def strategy(self):
        return self._strategy

    def enemy(self):
        return self._enemy

    def base_command(self):
        return self._base_command

    def army_command(self):
        return self._army_command

    async def on_start(self):
        await super().on_start()
        #constructor here as it is instanced automatically
        self._base_locations = []
        self._base_command = BaseCommand()
        self._army_command = ArmyCommand()
        self._strategy = EarlyGame()
        self._plan = LateGame()
        self._enemy = Enemy()
        await self.chat_send(f"strategy is ({self.strategy})")
        townhalls = self.townhalls()
        for t in townhalls:
            self._base_locations.append(t.position)
        #add locations to enemy
        self._enemy._base_locations.append(self.enemy_start_locations[0])
        self._enemy._base_locations.append(self.expansion_locations)

    async def on_step(self, iteration):
        #switch strategy
        if self._strategy._is_build_order_complete and not self._plan == "":
            self._strategy = self._plan
            self._plan = ""
            await self.chat_send(f"strategy is ({self.strategy})")

        ccs = self.townhalls()
        if iteration % 25 == 0:
            await self._base_command.redistribute_workers(self)
            #set has_base when no base left
            if not ccs:
                self.has_base = False
        
        await self._base_command.mule_down(self)

        
        
        if not self._strategy._is_build_order_complete:
            #build order
            await self._strategy.build_order(ccs, self)

        #industrialize
        await self._strategy.industrialize(ccs, self)

        #militarize
        await self._strategy.militarize(self)

        #attack or defend
        if self._strategy._army_command == "defensive":
            await self._army_command.defend(self, self._enemy)
        elif self._strategy._army_command == "offensive":
            await self._army_command.attack(self, self._enemy)
