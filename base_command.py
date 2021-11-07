from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.ids.ability_id import AbilityId

from command import Command

class BaseCommand(Command):

    async def build_gas_refineries(self, ccs, oops_bot):
    # Build refineries (on nearby vespene) when at least one barracks is in construction
        # Loop over all townhalls that are 100% complete
        for cc in ccs:
            vgs = []
            if cc.is_ready:
            # Find all vespene geysers that are closer than range 10 to this townhall
                vgs: Units = oops_bot.vespene_geyser.closer_than(10, cc)
            for vg in vgs:
                if await oops_bot.can_place_single(UnitTypeId.REFINERY, vg.position) and oops_bot.can_afford(UnitTypeId.REFINERY):
                    workers: Units = oops_bot.workers.gathering
                    if workers:  # same condition as above
                        worker: Unit = workers.closest_to(vg)
                        worker.build(UnitTypeId.REFINERY, vg)
                        # Dont build more than one each frame
                        break

    async def build_workers(self, cc, queue):
        cc = cc.get("cc")
        cc.train(UnitTypeId.SCV, queue=queue)

    async def redistribute_workers(self, oops_bot):
        await oops_bot.distribute_workers(resource_ratio=1)

    async def build_supply(self, oops_bot):
        ccs = oops_bot.townhalls()
        await oops_bot.build(UnitTypeId.SUPPLYDEPOT, near=ccs[0].position.towards(oops_bot.game_info.map_center, 4))

    async def builder(self, oops_bot, unit_id, distance):
        cc = oops_bot.base_locations[0]
        await oops_bot.build(unit_id, near=cc.position.towards(oops_bot.game_info.map_center, distance))


    #call mule
    async def mule_down(self, oops_bot):
        for oc in oops_bot.townhalls(UnitTypeId.ORBITALCOMMAND).filter(lambda x: x.energy >= 50):
            #minerals   
            mfs: Units = oops_bot.mineral_field.closer_than(10, oc)
            if mfs:
                mf: Unit = max(mfs, key=lambda x: x.mineral_contents)
                oc(AbilityId.CALLDOWNMULE_CALLDOWNMULE, mf)