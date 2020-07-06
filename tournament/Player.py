class Player(object):
    def __init__(self, name, agent_fn="random"):
        self.name = name
        self.agent_fn = agent_fn
