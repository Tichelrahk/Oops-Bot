from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit

from command import Command

class BaseCommand(Command):

    async def build_gas_refineries(self, ccs, OopsBot):
    # Build refineries (on nearby vespene) when at least one barracks is in construction
        # Loop over all townhalls that are 100% complete
        for cc in ccs:
            if cc.is_ready:
            # Find all vespene geysers that are closer than range 10 to this townhall
                vgs: Units = OopsBot.vespene_geyser.closer_than(10, cc)
            for vg in vgs:
                if await OopsBot.can_place_single(UnitTypeId.REFINERY, vg.position) and OopsBot.can_afford(UnitTypeId.REFINERY):
                    workers: Units = OopsBot.workers.gathering
                    if workers:  # same condition as above
                        worker: Unit = workers.closest_to(vg)
                        # Caution: the target for the refinery has to be the vespene geyser, not its position!
                        worker.build(UnitTypeId.REFINERY, vg)

                        # Dont build more than one each frame
                        break

    async def build_workers(self, cc):
        cc.train(UnitTypeId.SCV)

    async def redistribute_workers(self, OopsBot):
        await OopsBot.distribute_workers(resource_ratio=2)