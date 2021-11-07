import sys
from abc import ABC, abstractmethod

#From framework
from sc2.position import Point2
from sc2.bot_ai import BotAI


class GamePlayer(ABC):
    def __init__(self):
        self._base_locations = []
    
    def base_locations(self):
        return self._base_locations
        
    @abstractmethod
    def has_base(self):
        pass

