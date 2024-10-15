from agents.straight_man import StraightMan
from agents.fool import Fool
from agents.smart_alec import SmartAlec
from utils.openai_client import get_completion

class SceneManager:
    def __init__(self):
        self.agents = [StraightMan(), Fool(), SmartAlec()]
        self.scene_state = ""
        self.current_agent_index = 0
        self.suggestion = ""

    def start_scene(self, suggestion):
        self.suggestion = suggestion
        self.scene_state = ""
        self.current_agent_index = 0

        # Use OpenAI to set up the initial scene
        prompt = f"Given the suggestion '{suggestion}', create an initial setup for an improv scene. Establish the Who (relationship between characters), What (what they're doing), and Where (location). Also, include a way to 'raise the stakes' or create a problem that needs to be resolved."
        initial_setup = get_completion(prompt)

        self.scene_state += f"Suggestion: {suggestion}\n\nInitial Setup: {initial_setup}\n\n"
        return {"scene_state": self.scene_state}

    def next_turn(self):
        if self.is_scene_over():
            return {"scene_state": self.scene_state, "scene_over": True}

        current_agent = self.agents[self.current_agent_index]
        action = current_agent.ooda_loop(self.scene_state)

        self.scene_state += f"{action['agent']}: {action['action']}\n\n"
        self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)

        return {"scene_state": self.scene_state, "scene_over": False}

    def is_scene_over(self):
        # Check if the scene should end
        prompt = f"Given the following improv scene, determine if it has reached a satisfying conclusion or a funny crescendo. If so, respond with 'YES'. If not, respond with 'NO'.\n\nScene:\n{self.scene_state}"
        response = get_completion(prompt)
        return response.strip().upper() == "YES"
