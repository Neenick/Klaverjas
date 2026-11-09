from abc import ABC, abstractmethod

from cards import Card
from observation import Observation


class BaseAgent(ABC):

    @abstractmethod
    def select_card(self, observation: Observation) -> Card:
        """Select a card based on the available information."""
        pass
