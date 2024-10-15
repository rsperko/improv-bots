from .base_agent import BaseAgent
from utils.openai_client import get_completion

class StraightMan(BaseAgent):
    def __init__(self):
        super().__init__("Straight Man")
        self.personality = "You are the straight man in an improv scene. You are logical, serious, and often exasperated by the antics of others. Your role is to ground the scene and provide a foil for the other characters."
        self.scene_state = None
        self.response = None

    def observe(self, scene_state):
        self.scene_state = scene_state

    def orient(self):
        prompt = f"{self.personality}\n\nScene so far:\n{self.scene_state}\n\nHow do you react?"
        self.response = get_completion(prompt)

    def decide(self):
        # For simplicity, we'll just use the response as is
        pass

    def act(self):
        return {"agent": self.name, "action": self.response}
