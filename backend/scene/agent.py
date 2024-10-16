from utils import get_completion, get_model_prompt

class Agent:
    def __init__(self, name, personality, prompts):
        self.name = name
        self.personality = personality
        self.prompts = prompts
        self.character_name = None
        self.scene_state = None
        self.response = None

    def observe(self, context):
        self.scene_state = get_model_prompt(lambda model: self.prompts[model]['observe'].format(
            character_name=self.character_name,
            context=context
        ))

    def orient(self):
        self.response = get_completion(lambda model: self.prompts[model]['orient'].format(
            personality=self.personality,
            scene_state=self.scene_state
        ))

    def decide(self):
        # For simplicity, we'll just use the response as is
        pass

    def act(self):
        return {"agent": self.name, "action": self.response}

    def ooda_loop(self, context):
        self.observe(context)
        self.orient()
        self.decide()
        return {"action": self.response}
