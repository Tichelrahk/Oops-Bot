from strategy import Strategy
from base_command import BaseCommand
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.ids.ability_id import AbilityId
#from oops_bot import OopsBot

class EarlyGame(Strategy):
        def __init__(self):
            self._army_command = "defensive"
            self.is_build_order_complete = False
            self.build_order_check = 0

        async def build_order(self, ccs, oops_bot):
            
            #prioritize orbitals
            orbital_tech_requirement: float = oops_bot.tech_requirement_progress(UnitTypeId.ORBITALCOMMAND)
            if orbital_tech_requirement == 1:
                for cc in oops_bot.townhalls(UnitTypeId.COMMANDCENTER).idle:
                    if oops_bot.can_afford(UnitTypeId.ORBITALCOMMAND):
                        cc(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)

            if not self.is_build_order_complete and (oops_bot.already_pending(UnitTypeId.FACTORY) + oops_bot.structures(UnitTypeId.FACTORY).ready.amount) > 0:
                    self.is_build_order_complete = True
                    await oops_bot.chat_send(f"Build order finished")
                        
            if not self.is_build_order_complete:
                #standard build order
                if self.build_order_check == 0 and oops_bot.supply_workers >= 13 and oops_bot.can_afford(UnitTypeId.SUPPLYDEPOT) and oops_bot.already_pending(UnitTypeId.SUPPLYDEPOT) < 1:
                    await oops_bot.build(UnitTypeId.SUPPLYDEPOT, near=ccs[0].position.towards(oops_bot.game_info.map_center, 5))
                    self.build_order_check = 1
                    await oops_bot.chat_send(f"(building supply depot)")

                if self.build_order_check == 1 and oops_bot.structures(UnitTypeId.SUPPLYDEPOT).ready and oops_bot.can_afford(UnitTypeId.BARRACKS):
                    await oops_bot.build(UnitTypeId.BARRACKS, near=ccs[0].position.towards(oops_bot.game_info.map_center, 12))
                    self.build_order_check = 2
                    await oops_bot.chat_send(f"(building rax)")


                if self.build_order_check == 2 and oops_bot.can_afford(UnitTypeId.COMMANDCENTER) and (oops_bot.townhalls.amount) < 2:
                    await oops_bot.expand_now()
                    self.build_order_check = 3
                    await oops_bot.chat_send(f"(building expansion)")

                if oops_bot.can_afford(UnitTypeId.REFINERY) and (oops_bot.already_pending(UnitTypeId.REFINERY) + oops_bot.structures(UnitTypeId.REFINERY).ready.amount) < 1 and oops_bot.already_pending(UnitTypeId.BARRACKS):
                    await oops_bot.base_command.build_gas_refineries(ccs, oops_bot)

                for b in oops_bot.structures(UnitTypeId.BARRACKS).ready.idle:
                    if self.build_order_check >= 2 and oops_bot.can_afford(UnitTypeId.BARRACKSTECHLAB) and not b.has_add_on and oops_bot.structures(UnitTypeId.BARRACKSTECHLAB).amount < 1:
                        b.build(UnitTypeId.BARRACKSTECHLAB)
                        await oops_bot.chat_send(f"(building techlab)")

                if oops_bot.can_afford(UnitTypeId.REFINERY) and (oops_bot.already_pending(UnitTypeId.REFINERY) + oops_bot.structures(UnitTypeId.REFINERY).ready.amount) < 4 and oops_bot.structures(UnitTypeId.BARRACKS).ready:
                    await oops_bot.base_command.build_gas_refineries(ccs, oops_bot)

                if self.build_order_check >= 3 and oops_bot.can_afford(UnitTypeId.FACTORY) and  (oops_bot.already_pending(UnitTypeId.FACTORY) + oops_bot.structures(UnitTypeId.FACTORY).ready.amount) < 2:
                    await oops_bot.build(UnitTypeId.FACTORY, near=ccs[0].position.towards(oops_bot.game_info.map_center, 10))
                    await oops_bot.chat_send(f"(building factory)")

                

        async def industrialize(self, ccs, oops_bot):
            # Build workers
            for cc in ccs:
                surplus_harvesters = cc.surplus_harvesters
                if oops_bot.can_afford(UnitTypeId.SCV) and surplus_harvesters < 0 and cc.is_idle:
                    await oops_bot.base_command.build_workers(cc)
            #build depots
            if (
                oops_bot.supply_left < (3 if oops_bot.structures(UnitTypeId.BARRACKS).amount < 3 else 5) and oops_bot.supply_used >= 14
            ):
                if oops_bot.can_afford(UnitTypeId.SUPPLYDEPOT) and oops_bot.already_pending(UnitTypeId.SUPPLYDEPOT) < 1:
                    await oops_bot.build(UnitTypeId.SUPPLYDEPOT, near=ccs[0].position.towards(oops_bot.game_info.map_center, 4))

            if self.is_build_order_complete:
                if oops_bot.can_afford(UnitTypeId.REFINERY) and (oops_bot.already_pending(UnitTypeId.REFINERY) + oops_bot.structures(UnitTypeId.REFINERY).ready.amount) < 4:
                    await oops_bot.base_command.build_gas_refineries(ccs, oops_bot)

                if oops_bot.can_afford(UnitTypeId.BARRACKS) and (oops_bot.already_pending(UnitTypeId.BARRACKS) + oops_bot.structures(UnitTypeId.BARRACKS).ready.amount) < 4:
                    p: Point2 = ccs[0].position.towards(oops_bot.enemy_start_locations[0], 14)
                    await oops_bot.build(UnitTypeId.BARRACKS, near=p)

                if oops_bot.can_afford(UnitTypeId.STARPORT) and (oops_bot.already_pending(UnitTypeId.STARPORT) + oops_bot.structures(UnitTypeId.STARPORT).ready.amount) < 2:
                    p: Point2 = ccs[0].position.towards(oops_bot.enemy_start_locations[0], 8)
                    await oops_bot.build(UnitTypeId.STARPORT, near=p)

                for rax in oops_bot.structures(UnitTypeId.BARRACKS).ready.idle:
                    if not rax.has_techlab and oops_bot.can_afford(UnitTypeId.BARRACKSREACTOR):
                        rax.build(UnitTypeId.BARRACKSREACTOR)




        async def militarize(self, oops_bot):
            # Train marines and marauders
            for rax in oops_bot.structures(UnitTypeId.BARRACKS).ready.idle:
                if rax.has_techlab and oops_bot.can_afford(UnitTypeId.MARAUDER):
                    rax.train(UnitTypeId.MARAUDER)
                elif oops_bot.can_afford(UnitTypeId.MARINE):
                    rax.train(UnitTypeId.MARINE)

            #Train medivacs
            for sp in oops_bot.structures(UnitTypeId.STARPORT).ready.idle:
                if oops_bot.can_afford(UnitTypeId.MEDIVAC) and oops_bot.units(UnitTypeId.MEDIVAC).idle.amount < 12:
                    sp.train(UnitTypeId.MEDIVAC)