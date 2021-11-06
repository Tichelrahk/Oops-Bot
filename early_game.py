from strategy import Strategy
from base_command import BaseCommand
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.bot_ai import BotAI
#from oops_bot import OopsBot

class EarlyGame(Strategy):
        def __init__(self):
            self._army_command = "defensive"
            self._end_game_conditions = "false"

        async def build_order(self, ccs, oops_bot):
            # Build Refineries
            if (oops_bot.structures(UnitTypeId.BARRACKS).ready.amount + oops_bot.already_pending(UnitTypeId.BARRACKS) > 0 and oops_bot.already_pending(UnitTypeId.REFINERY) < 1 and oops_bot.structures(UnitTypeId.REFINERY).ready.amount < 1):
                await oops_bot.base_command.build_gas_refineries(ccs, oops_bot)
            
            # Build more depots
            elif (
                oops_bot.supply_left < (3 if oops_bot.structures(UnitTypeId.BARRACKS).amount < 3 else 4) and oops_bot.supply_used >= 14
            ):
                if oops_bot.can_afford(UnitTypeId.SUPPLYDEPOT) and oops_bot.already_pending(UnitTypeId.SUPPLYDEPOT) < 1:
                    await oops_bot.build(UnitTypeId.SUPPLYDEPOT, near=ccs[0].position.towards(oops_bot.game_info.map_center, 5))

            # Build proxy barracks
            elif oops_bot.structures(UnitTypeId.BARRACKS).amount < 3 or (oops_bot.minerals > 400 and oops_bot.structures(UnitTypeId.BARRACKS).amount < 8):
                if oops_bot.can_afford(UnitTypeId.BARRACKS):
                    p: Point2 = oops_bot.game_info.map_center.towards(oops_bot.enemy_start_locations[0], 25)
                    await oops_bot.build(UnitTypeId.BARRACKS, near=p)

        def industrialize(self, ccs, base_command, oops_bot):
            pass

        def militarize():
            pass