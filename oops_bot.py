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



class OopsBot(GamePlayer):

    async def on_start(self):
        await super().on_start()
        self.base_command = BaseCommand()
        await self.chat_send(f"(GLHF)")
        self.strategy = EarlyGame()

    async def on_step(self, iteration):
        #if iteration == 4:
            #if self.has_base():
                #await self.chat_send(f"I have a base")

        # If we don't have a townhall anymore, send all units to attack
        ccs: Units = self.townhalls(UnitTypeId.COMMANDCENTER)
        if not ccs:
            target: Point2 = self.enemy_structures.random_or(self.enemy_start_locations[0]).position
            for unit in self.workers | self.units(UnitTypeId.MARINE):
                unit.attack(target)
            return


        #build order
        await self.strategy.build_order(ccs, self)

        # Send marines in waves of 15, each time 15 are idle, send them to their death
        marines: Units = self.units(UnitTypeId.MARINE).idle
        if marines.amount > 15:
            target: Point2 = self.enemy_structures.random_or(self.enemy_start_locations[0]).position
            for marine in marines:
                marine.attack(target)

        # Train more SCVs
        #build workers based on gathering workers near command center
        for cc in ccs:
            surplus_harvesters = cc.surplus_harvesters
            if self.can_afford(UnitTypeId.SCV) and surplus_harvesters < 0 and cc.is_idle:
                await self.base_command.build_workers(cc)

        # Train marines
        for rax in self.structures(UnitTypeId.BARRACKS).ready.idle:
            if self.can_afford(UnitTypeId.MARINE):
                rax.train(UnitTypeId.MARINE)

        # Send idle workers to gather minerals near command center
        for scv in self.workers.idle:
            scv.gather(self.mineral_field.closest_to(cc))

        if (
            self.structures(UnitTypeId.REFINERY).ready.amount >= 1
        ):
            await self.base_command.redistribute_workers(self)