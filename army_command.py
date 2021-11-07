from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
import random

from command import Command

class ArmyCommand(Command):

    async def defend(self, oops_bot, enemy):
        # If we don't have a townhall anymore, desperate attack
        ccs: Units = oops_bot.townhalls
        if not ccs:
            target: Point2 = enemy_structures.random_or(enemy._base_locations[0]).position
            for unit in self.workers | self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER):
                unit.attack(target)
            return

        #stay by the furthest building
        marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
        marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
        medivacs: Units = oops_bot.units(UnitTypeId.MEDIVAC).idle
        enemy_location = enemy._base_locations[0].position
        far_building = oops_bot.structures.closest_to(enemy_location)
        if marines.amount > 1:
            far_marine = marines.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marine)
        for marine in marines:
            marine.move(far_building.position.towards(oops_bot._base_locations[-1], 5))
            marine.stop
        for marauder in marauders:
            marauder.move(far_building.position.towards(oops_bot._base_locations[-1], 5))
            marauder.stop

    async def attack(self, oops_bot, enemy):

        # If we don't have a townhall anymore, desperate attack
        if not oops_bot.has_base:
            target: Point2 = oops_bot.enemy_structures.random_or(enemy._base_locations[0])
            for unit in oops_bot.workers | oops_bot.units(UnitTypeId.MARINE) | oops_bot.units(UnitTypeId.MARAUDER):
                unit.attack(target)
            return

        #gather by furthest building
        marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
        marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
        medivacs: Units = oops_bot.units(UnitTypeId.MEDIVAC).idle
        enemy_location = enemy._base_locations[0]
        far_building = oops_bot.structures.closest_to(enemy_location)
        if marines.amount > 1:
            far_marine = marines.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marine)
        for marine in marines:
            marine.move(far_building.position.towards(oops_bot._base_locations[-1], 5))
            marine.stop
        for marauder in marauders:
            marauder.move(far_building.position.towards(oops_bot._base_locations[-1], 5))
            marauder.stop

        #attacks
        #medivac handling
        marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
        marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
        medivacs: Units = oops_bot.units(UnitTypeId.MEDIVAC).idle
        enemy_location = enemy._base_locations[0]
        if marines.amount > 1:
            far_marine = marines.closest_to(enemy_location)
            for medi in medivacs:
                medi.move(far_marine)
        #more combat than support
        army = marines.amount + marauders.amount + (medivacs.amount * 0.5)

        #last hunt
        #change back to 185
        if oops_bot.supply_used > 185:
            await oops_bot.chat_send(f"I'm hunting!")
            target: Point2 = random.choice(oops_bot.expansion_locations_list)
            marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
            marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
            vs: Units = oops_bot.units(UnitTypeId.VIKINGFIGHTER).idle
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)
            for v in vs:
                v.attack(target)
        #very big army
        elif oops_bot.supply_army > 70:
            await oops_bot.chat_send(f"I'm attacking! BIG")
            target: Point2 = oops_bot.enemy_structures.random_or(enemy_location).position
            marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
            marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)

        #big army/fast reinforcements
        elif oops_bot.supply_used > 90:
            if army > 40:
                await oops_bot.chat_send(f"I'm attacking! mid")
                target: Point2 = oops_bot.enemy_structures.random_or(enemy_location).position
                marines: Units = oops_bot.units(UnitTypeId.MARINE).idle
                marauders: Units = oops_bot.units(UnitTypeId.MARAUDER).idle
                for marine in marines:
                    marine.attack(target)
                for marauder in marauders:
                    marauder.attack(target)

        #early/small army
        elif army > 25 and oops_bot.supply_used < 90:
            await oops_bot.chat_send(f"I'm attacking small!")
            target: Point2 = oops_bot.enemy_structures.random_or(enemy_location).position
            marines: Units = oops_bot.units(UnitTypeId.MARINE)
            marauders: Units = oops_bot.units(UnitTypeId.MARAUDER)
            for marine in marines:
                marine.attack(target)
            for marauder in marauders:
                marauder.attack(target)
        