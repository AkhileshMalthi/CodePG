from abc import ABC, abstractmethod

class Generator(ABC):

    @abstractmethod
    def generate(self, prompt):
        """generates response for the prompt"""
        pass

    @abstractmethod
    def __str__(self):
        """returns generator information"""
        pass


