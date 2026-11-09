import random

from agents.base_agent import BaseAgent
from cards import Card
from observation import Observation


class RandomAgent(BaseAgent):

    def select_card(self, observation: Observation) -> Card:
        return random.choice(observation.legal_cards)
