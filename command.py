from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit

class Command():
	async def immediate(self, command, **kwargs):
		await command(kwargs, queue=True)

	async def queue(self, command, **kwargs):
		await command(kwargs, queue=True)