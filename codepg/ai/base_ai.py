from abc import ABC, abstractmethod

class AI(ABC):
    @abstractmethod
    def generate(self, programming_language: str, prompt: str) -> str:
        """generates code in specified language based on the prompt"""
        pass

    @abstractmethod
    def __str__(self):
        """returns generator information"""
        pass


