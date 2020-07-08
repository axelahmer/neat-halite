from halite.inputs import *
from kaggle_environments import make
from kaggle_environments.envs.halite.helpers import *

board_size = 3
environment = make("halite", configuration={"size": board_size, "startingHalite": 5000, "agentExec": "LOCAL"})
agent_count = 1
environment.reset(agent_count)

observation = environment.state[0].get("observation")
configuration = environment.configuration
board = Board(observation, configuration)
me = board.current_player

result = cell_radar(me.ships[0].cell, 1)

print(board)

print("")

