from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit

class Command():
	def immediate(command, *args):
		command(queue=False, *args)

	def queue(command, *args):
		command(queue=True, *args)