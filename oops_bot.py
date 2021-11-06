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

    async def on_start(self):
        await super().on_start()
        #constructor here as it is instanced automatically
        self.base_locations = []
        self.base_command = BaseCommand()
        self.army_command = ArmyCommand()
        self.strategy = EarlyGame()
        self.plan = LateGame()
        self.enemy = Enemy()
        await self.chat_send(f"strategy is ({self.strategy})")
        townhalls = self.townhalls()
        for t in townhalls:
            self.base_locations.append(t.position)
        #add locations to enemy
        self.enemy.base_locations.append(self.enemy_start_locations[0])
        self.enemy.base_locations.append(self.expansion_locations)

    async def on_step(self, iteration):
        #switch strategy
        if self.strategy.is_build_order_complete and not self.plan == "":
            self.strategy = self.plan
            self.plan = ""
            await self.chat_send(f"strategy is ({self.strategy})")

        ccs = self.townhalls()
        if iteration % 25 == 0:
            await self.distribute_workers()
            #set has_base when no base left
            if not ccs:
                self.has_base = False
        
        await self.base_command.mule_down(self)

        
        
        if not self.strategy.is_build_order_complete:
            #build order
            await self.strategy.build_order(ccs, self)

        #industrialize
        await self.strategy.industrialize(ccs, self)

        #militarize
        await self.strategy.militarize(self)

        #attack or defend
        if self.strategy.army_command == "defensive":
            await self.army_command.defend(self, self.enemy)
        elif self.strategy.army_command == "offensive":
            await self.army_command.attack(self, self.enemy)

        
        

        