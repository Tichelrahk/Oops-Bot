from abc import ABC, abstractmethod

class Strategy(ABC):
    @property
    def army_command(self):
        return self._army_command
    
    @abstractmethod
    def industrialize(self):
        pass

    @abstractmethod
    def militarize():
        pass