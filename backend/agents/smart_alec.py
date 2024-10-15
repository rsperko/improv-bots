from .base_agent import BaseAgent
from utils.openai_client import get_completion

class SmartAlec(BaseAgent):
    def __init__(self):
        super().__init__("Smart Alec")
        self.personality = "You are the smart alec in an improv scene. You are witty, sarcastic, and always ready with a clever remark. Your role is to provide commentary and add layers of humor to the scene."
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
