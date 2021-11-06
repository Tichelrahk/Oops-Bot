from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
import random

from command import Command

class ArmyCommand(Command):

    async def defend(self, oops_bot, enemy):
        # If we don't have a townhall anymore, desperate attack
        ccs: Units = oops_bot.townhalls
        if not ccs:
            target: Point2 = oops_bot.enemy_structures.random_or(enemy.base_locations[0]).position
            for unit in self.workers | self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER):
                unit.attack(target)
            return

        #stay by the furthest building
        marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
        marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
        medivacs: Units = oops_bot.units(UnitTypeId.MEDIVAC).idle
        enemy_location = enemy.base_locations[0].position
        far_building = oops_bot.structures.closest_to(enemy_location)
        if marines.amount > 1:
            far_marine = marines.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marine)
        for marine in marines:
            marine.move(far_building.position.towards(oops_bot.base_locations[-1], 5))
            marine.stop
        for marauder in marauders:
            marauder.move(far_building.position.towards(oops_bot.base_locations[-1], 5))
            marauder.stop

    async def attack(self, oops_bot, enemy):

        # If we don't have a townhall anymore, desperate attack
        if not oops_bot.has_base:
            target: Point2 = enemy.enemy_structures.random_or(enemy.base_locations[0])
            for unit in self.workers | self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER):
                unit.attack(target)
            return

        #gather by furthest building
        marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
        marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
        medivacs: Units = oops_bot.units(UnitTypeId.MEDIVAC).idle
        enemy_location = enemy.base_locations[0]
        far_building = oops_bot.structures.closest_to(enemy_location)
        if marines.amount > 1:
            far_marine = marines.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marine)
        for marine in marines:
            marine.move(far_building.position.towards(oops_bot.base_locations[-1], 5))
            marine.stop
        for marauder in marauders:
            marauder.move(far_building.position.towards(oops_bot.base_locations[-1], 5))
            marauder.stop

        #attacks
        #medivac handling
        marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
        marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
        medivacs: Units = oops_bot.units(UnitTypeId.MEDIVAC).idle
        enemy_location = enemy.base_locations[0]
        if marines.amount > 1:
            far_marine = marines.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marine)
        elif marauders.amount > 1:
            far_marauder = marauders.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marauder)
        #more combat than support
        army = marines.amount + marauders.amount + (medivacs.amount * 0.5)

        #very big army
        if oops_bot.supply_army > 60:
            await oops_bot.chat_send(f"I'm attacking! BIG")
            target: Point2 = oops_bot.enemy_structures.random_or(enemy_location).position
            marines: Units = oops_bot.units(UnitTypeId.MARINE)
            marauders: Units = oops_bot.units(UnitTypeId.MARAUDER)
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)

        #big army/fast reinforcements
        elif oops_bot.supply_used > 90:
            if army > 40:
                await self.chat_send(f"I'm attacking! mid")
                target: Point2 = oops_bot.enemy_structures.random_or(enemy_location).position
                marines: Units = oops_bot.units(UnitTypeId.MARINE)
                marauders: Units = oops_bot.units(UnitTypeId.MARAUDER)
                for marine in marines:
                    marine.attack(target)
                for marauder in marauders:
                    marauder.attack(target)

        #early/small army
        elif army > 20:
            await oops_bot.chat_send(f"I'm attacking small!")
            target: Point2 = oops_bot.enemy_structures.random_or(enemy_location).position
            marines: Units = oops_bot.units(UnitTypeId.MARINE)
            marauders: Units = oops_bot.units(UnitTypeId.MARAUDER)
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)
        #end hunt
        elif oops_bot.supply_used > 180:
            await oops_bot.chat_send(f"I'm hunting!")
            target: Point2 = random.choice(enemy.base_locations)
            marines: Units = oops_bot.units(UnitTypeId.MARINE)
            marauders: Units = oops_bot.units(UnitTypeId.MARAUDER)
            vs: Units = oops_bot.units(UnitTypeId.VALKYRIE)
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)
            for v in vs:
                v.attack(target)