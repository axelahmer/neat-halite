from kaggle_environments import make
import concurrent.futures
import time


def run_game(name):
    print(f'starting {name}')
    th1 = time.time()
    board_size = 21
    environment = make("halite", configuration={"size": board_size, "startingHalite": 5000, "agentExec": "LOCAL"})
    agent_count = 4
    environment.reset(agent_count)
    environment.run(["random", "random", "random", "random"])
    # environment.render(mode="ansi", width=500, height=450)
    th2 = time.time()
    scores = [agent.reward for agent in environment.steps[-1]]

    print(f'{name} running time: {th2 - th1}')
    return scores


if __name__ == "__main__":
    t1 = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = executor.map(run_game, range(8))

    results = [f for f in futures]
    t2 = time.time()
    print(f'main running time: {t2 - t1}')
    print(results)
