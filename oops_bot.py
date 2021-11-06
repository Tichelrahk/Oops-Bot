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
from early_game import EarlyGame
from late_game import LateGame



class OopsBot(GamePlayer):

    async def on_start(self):
        await super().on_start()
        self.base_command = BaseCommand()
        self.strategy = EarlyGame()
        self.plan = LateGame()
        await self.chat_send(f"strategy is ({self.strategy})")

    async def on_step(self, iteration):
        #switch strategy
        if self.strategy.is_build_order_complete and not self.plan == "":
            self.strategy = self.plan
            self.plan = ""
            await self.chat_send(f"strategy is ({self.strategy})")


        # If we don't have a townhall anymore, send all units to attack
        ccs: Units = self.townhalls
        if not ccs:
            target: Point2 = self.enemy_structures.random_or(self.enemy_start_locations[0]).position
            for unit in self.workers | self.units(UnitTypeId.MARINE):
                unit.attack(target)
            return

        if iteration % 25 == 0:
            await self.distribute_workers()

        
        await self.base_command.mule_down(self)
        
        if not self.strategy.is_build_order_complete:
            #build order
            await self.strategy.build_order(ccs, self)

        #industrialize
        await self.strategy.industrialize(ccs, self)

        #militarize
        await self.strategy.militarize(self)

        
        marines: Units = self.units(UnitTypeId.MARINE).idle
        marauders: Units = self.units(UnitTypeId.MARAUDER).idle
        medivacs: Units = self.units(UnitTypeId.MEDIVAC).idle
        enemy_location = self.enemy_start_locations[0]
        if marines.amount > 1:
            far_marine = marines.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marine)
        far_building = self.structures.closest_to(enemy_location)
        for marine in marines:
            marine.move(far_building.position.towards(self.base_locations[-1], 10))
            marine.stop
        for marauder in marauders:
            marauder.move(far_building.position.towards(self.base_locations[-1], 10))
            marauder.stop
        army = marines.amount + marauders.amount + (medivacs.amount * 0.5)
        if self.supply_army > 60:
            await self.chat_send(f"I'm attacking!'")
            target: Point2 = self.enemy_structures.random_or(enemy_location).position
            marines: Units = self.units(UnitTypeId.MARINE)
            marauders: Units = self.units(UnitTypeId.MARAUDER)
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)
        elif self.supply_used > 90:
            if army > 40:
                await self.chat_send(f"I'm attacking!'")
                target: Point2 = self.enemy_structures.random_or(enemy_location).position
                marines: Units = self.units(UnitTypeId.MARINE)
                marauders: Units = self.units(UnitTypeId.MARAUDER)
                for marine in marines:
                    marine.attack(target)
                for marauder in marauders:
                    marauder.attack(target)
        elif army > 20:
            await self.chat_send(f"I'm attacking!'")
            target: Point2 = self.enemy_structures.random_or(enemy_location).position
            marines: Units = self.units(UnitTypeId.MARINE)
            marauders: Units = self.units(UnitTypeId.MARAUDER)
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)

        