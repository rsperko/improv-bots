from agents.straight_man import StraightMan
from agents.fool import Fool
from agents.smart_alec import SmartAlec
from utils.openai_client import get_completion
import json

class SceneManager:
    def __init__(self):
        self.agents = [StraightMan(), Fool(), SmartAlec()]
        self.scene_state = {
            "suggestion": "",
            "who": "",
            "what": "",
            "where": "",
            "problem": "",
            "actions": []
        }
        self.current_agent_index = 0
        self.character_names = []

    def start_scene(self, suggestion):
        prompt = f"""Given the suggestion '{suggestion}', create an initial setup for an improv scene.
        Return a JSON object with the following structure:
        {{
            "who": "Describe the relationship between characters",
            "what": "Describe what they are doing",
            "where": "Describe the location",
            "problem": "Describe the problem or how to raise the stakes",
            "character_names": ["Name for Straight Man", "Name for Fool", "Name for Smart Alec"],
            "initial_action": "Provide the first line of dialogue or action for the first character"
        }}
        """
        initial_setup = get_completion(prompt)

        try:
            setup_data = json.loads(initial_setup)
            self.character_names = setup_data["character_names"]
            self.scene_state = {
                "suggestion": suggestion,
                "who": setup_data["who"],
                "what": setup_data["what"],
                "where": setup_data["where"],
                "problem": setup_data["problem"],
                "actions": [{"agent": self.character_names[0], "action": setup_data["initial_action"]}]
            }
        except json.JSONDecodeError:
            # Fallback in case the AI doesn't return valid JSON
            self.character_names = ["Character 1", "Character 2", "Character 3"]
            self.scene_state = {
                "suggestion": suggestion,
                "who": "Unknown",
                "what": "Unknown",
                "where": "Unknown",
                "problem": "Unknown",
                "actions": [{"agent": self.character_names[0], "action": initial_setup}]
            }

        return self.scene_state

    def next_turn(self):
        if self.is_scene_over():
            return {"scene_state": self.scene_state, "scene_over": True}

        current_agent = self.agents[self.current_agent_index]
        action = current_agent.ooda_loop(self._get_scene_context())

        self.scene_state["actions"].append({
            "agent": self.character_names[self.current_agent_index],
            "action": action['action']
        })
        self.current_agent_index = (self.current_agent_index + 1) % len(self.agents)

        return {"scene_state": self.scene_state, "scene_over": False}

    def is_scene_over(self):
        prompt = f"Given the following improv scene, determine if it has reached a satisfying conclusion or a funny crescendo. If so, respond with 'YES'. If not, respond with 'NO'.\n\nScene:\n{self._get_scene_context()}"
        response = get_completion(prompt)
        return response.strip().upper() == "YES"

    def _get_scene_context(self):
        context = f"Suggestion: {self.scene_state['suggestion']}\n"
        context += f"Who: {self.scene_state['who']}\n"
        context += f"What: {self.scene_state['what']}\n"
        context += f"Where: {self.scene_state['where']}\n"
        context += f"Problem: {self.scene_state['problem']}\n\n"
        context += "\n".join([f"{action['agent']}: {action['action']}" for action in self.scene_state['actions']])
        return context
