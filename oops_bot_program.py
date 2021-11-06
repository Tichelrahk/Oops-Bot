import os
import sys

#From framework
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from sc2 import maps
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer

#From Project
from oops_bot import OopsBot

def main():
    run_game(
        maps.get("AcropolisLE"),
        [Bot(Race.Terran, OopsBot()), Computer(Race.Zerg, Difficulty.Hard)],
        realtime=False,
    )


if __name__ == "__main__":
    main()
