from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def observe(self, scene_state):
        pass

    @abstractmethod
    def orient(self):
        pass

    @abstractmethod
    def decide(self):
        pass

    @abstractmethod
    def act(self):
        pass

    def ooda_loop(self, scene_state):
        self.observe(scene_state)
        self.orient()
        self.decide()
        return self.act()
