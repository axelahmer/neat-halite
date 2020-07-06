import tournament.Player
from kaggle_environments import make


def halite_game(players):
    print('starting a game')
    agents = [player.agent_fn for player in players]
    environment = make("halite")
    agent_count = len(agents)
    environment.reset(agent_count)
    environment.run(agents)
    # environment.render(mode="ansi", width=500, height=450)
    rewards = [agent.reward for agent in environment.steps[-1]]
    print(f'game finished: {rewards}')
    return rewards
