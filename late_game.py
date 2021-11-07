from strategy import Strategy
from base_command import BaseCommand
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
#from oops_bot import OopsBot

class LateGame(Strategy):
        def __init__(self):
            self._army_command = "offensive"
            self.is_build_order_complete = True

        async def industrialize(self, ccs, oops_bot):
            #prioritize orbitals
            orbital_tech_requirement: float = oops_bot.tech_requirement_progress(UnitTypeId.ORBITALCOMMAND)
            if orbital_tech_requirement == 1:
                for cc in oops_bot.townhalls(UnitTypeId.COMMANDCENTER).idle:
                    if oops_bot.can_afford(UnitTypeId.ORBITALCOMMAND):
                        cc(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)

            # Build workers
            for cc in ccs:
                surplus_harvesters = cc.surplus_harvesters
                if oops_bot.can_afford(UnitTypeId.SCV) and surplus_harvesters < 0 and cc.is_idle and oops_bot.units(UnitTypeId.SCV).amount < 60 or (oops_bot.supply_used < 185 and oops_bot.supply_workers < 10):
                    await oops_bot.base_command.immediate(oops_bot.base_command.build_workers, cc=cc)
            #build depots
            if (oops_bot.supply_left < 10):
                if oops_bot.can_afford(UnitTypeId.SUPPLYDEPOT) and oops_bot.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
                    await oops_bot.base_command.build_supply(oops_bot)
            #build gas
            if oops_bot.can_afford(UnitTypeId.REFINERY) and (oops_bot.already_pending(UnitTypeId.REFINERY) + oops_bot.structures(UnitTypeId.REFINERY).ready.amount) < 4:
                await oops_bot.base_command.build_gas_refineries(ccs, oops_bot)
            
            #build expansion
            if (oops_bot.minerals > 600 and oops_bot.townhalls.amount < 4 and oops_bot.already_pending(UnitTypeId.COMMANDCENTER) < 1) or (oops_bot.minerals > 1400 and oops_bot.townhalls.amount < 16):
                await oops_bot.expand_now()
                await oops_bot.chat_send(f"(building expansion)")

            if oops_bot.can_afford(UnitTypeId.BARRACKS) and (oops_bot.already_pending(UnitTypeId.BARRACKS) + oops_bot.structures(UnitTypeId.BARRACKS).ready.amount) < 6 or (oops_bot.minerals > 1000 and oops_bot.structures(UnitTypeId.BARRACKS).ready.amount < 16):
                p: Point2 = ccs[0].position.towards(oops_bot.enemy_start_locations[0], 14)
                await oops_bot.base_command.builder(oops_bot, UnitTypeId.BARRACKS, 12)

            if oops_bot.can_afford(UnitTypeId.STARPORT) and (oops_bot.already_pending(UnitTypeId.STARPORT) + oops_bot.structures(UnitTypeId.STARPORT).ready.amount) < 2:
                p: Point2 = ccs[0].position.towards(oops_bot.enemy_start_locations[0], 8)
                await oops_bot.base_command.builder(oops_bot, UnitTypeId.STARPORT, 8)

            for rax in oops_bot.structures(UnitTypeId.BARRACKS).ready.idle:
                if not rax.has_techlab and oops_bot.can_afford(UnitTypeId.BARRACKSREACTOR):
                    rax.build(UnitTypeId.BARRACKSREACTOR)

        async def militarize(self, oops_bot):
            if oops_bot.supply_used < 185:
                # Train marines and marauders
                for rax in oops_bot.structures(UnitTypeId.BARRACKS).ready.idle:
                    if rax.has_techlab and oops_bot.can_afford(UnitTypeId.MARAUDER):
                        rax.train(UnitTypeId.MARAUDER)
                    elif oops_bot.can_afford(UnitTypeId.MARINE):
                        rax.train(UnitTypeId.MARINE)
                #Train medivacs
                for sp in oops_bot.structures(UnitTypeId.STARPORT).ready.idle:
                    if oops_bot.can_afford(UnitTypeId.MEDIVAC) and oops_bot.units(UnitTypeId.MEDIVAC).amount < 8:
                        sp.train(UnitTypeId.MEDIVAC)
            elif oops_bot.supply_used > 185:
                for sp in oops_bot.structures(UnitTypeId.STARPORT).ready.idle:
                    if oops_bot.can_afford(UnitTypeId.VIKINGFIGHTER) and oops_bot.units(UnitTypeId.VIKINGFIGHTER).amount < 10:
                        sp.train(UnitTypeId.VIKINGFIGHTER)