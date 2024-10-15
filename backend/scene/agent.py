from utils.openai_client import get_completion

class Agent:
    def __init__(self, name, description, personality):
        self.name = name
        self.personality = personality
        self.character_name = None
        self.scene_state = None
        self.response = None

    def observe(self, scene_state):
        pass

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


    def ooda_loop(self, character, context):
        prompt = f"""
        You are {character}. Respond to the current scene with a single action or line of dialogue.
        Do not describe actions for other characters or narrate the scene. Only describe your own actions or speech.
        Current scene:
        {context}
        """

        self.observe(prompt)
        self.orient()
        self.decide()
        return {"action": self.response}
