from utils import get_completion
from .agent import Agent
import yaml
import json
import random

class SceneManager:
    def __init__(self):
        self.agents = self._load_agents_from_yaml()
        self.prompts = self._load_prompts_from_yaml()
        self.scene_state = {
            "suggestion": "",
            "who": "",
            "what": "",
            "where": "",
            "problem": "",
            "actions": []
        }
        self.current_agent_index = 0

    def start_scene(self, suggestion):
        initial_setup = get_completion(lambda model: self.prompts[model]['start_scene'].format(
            suggestion=suggestion
        ))

        try:
            setup_data = json.loads(initial_setup)
            # loop through agents and set their names
            for agent in self.agents:
                agent.character_name = setup_data["character_names"].pop(0)
            self.scene_state = {
                "suggestion": suggestion,
                "who": setup_data["who"],
                "what": setup_data["what"],
                "where": setup_data["where"],
                "problem": setup_data["problem"],
                "actions": [{"agent_id": self.current_agent_index, "agent": self._current_agent().character_name, "action": setup_data["initial_action"]}]
            }
        except json.JSONDecodeError:
            # Fallback in case the AI doesn't return valid JSON
            self.scene_state = {
                "suggestion": suggestion,
                "who": "Unknown",
                "what": "Unknown",
                "where": "Unknown",
                "problem": "Unknown",
                "actions": [{"agent_id": self.current_agent_index, "agent": self._current_agent().character_name, "action": initial_setup}]
            }

        return self.scene_state

    def next_turn(self):
        if self.is_scene_over():
            return {"scene_state": self.scene_state, "scene_over": True}

        self.current_agent_index = random.randint(0, len(self.agents) - 1)

        current_agent = self._current_agent()

        action = current_agent.ooda_loop(self._get_scene_context())

        self.scene_state["actions"].append({
            "agent_id": self.current_agent_index,
            "agent": current_agent.character_name,
            "action": action['action']
        })

        return {"scene_state": self.scene_state, "scene_over": False}

    def is_scene_over(self):
        response = get_completion(lambda model: self.prompts[model]['is_scene_over'].format(
            context=self._get_scene_context()
        ))
        return response.strip().upper() == "YES"

    def _current_agent(self):
        return self.agents[self.current_agent_index]

    def _load_agents_from_yaml(self):
        with open('scene/agents.yaml', 'r') as file:
            agent_data = yaml.safe_load(file)['agents']
        return [Agent(**agent_info) for agent_info in agent_data]

    def _load_prompts_from_yaml(self):
        with open('scene/scene.yaml', 'r') as file:
            return yaml.safe_load(file)['prompts']

    def _get_scene_context(self):
        context = f"Suggestion: {self.scene_state['suggestion']}\n"
        context += f"Who: {self.scene_state['who']}\n"
        context += f"What: {self.scene_state['what']}\n"
        context += f"Where: {self.scene_state['where']}\n"
        context += f"Problem: {self.scene_state['problem']}\n\n"
        context += "\n".join([f"{action['agent']}: {action['action']}" for action in self.scene_state['actions']])
        return context
