from kaggle_environments.envs.halite.helpers import *


def agent(observation, configuration):
    board = Board(observation, configuration)
    cp = board.current_player
    desired_ships = 4

    # GO NORTH
    for ship in cp.ships:
        ship.next_action = ShipAction.NORTH

    # make shipyard if no yards
    if len(cp.ships) == 1 and len(cp.shipyards) == 0:
        cp.ships[0].next_action = ShipAction.CONVERT

    # make ship if no ships and have ship yard
    elif len(cp.shipyards) >= 1 and len(cp.ships) < desired_ships:
        cp.shipyards[0].next_action = ShipyardAction.SPAWN

    #     print(cp.halite)
    return cp.next_actions
