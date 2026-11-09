import random

from agents.base_agent import BaseAgent
from cards import Card
from observation import Observation


class RandomAgent(BaseAgent):

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def select_card(self, observation: Observation) -> Card:
        if not observation.legal_cards:
            raise ValueError("No legal cards available.")

        return self.rng.choice(observation.legal_cards)
