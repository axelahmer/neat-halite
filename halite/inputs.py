from kaggle_environments.envs.halite.helpers import *
import numpy as np


# file for determining NN inputs

def cell_radar_radius(origin: Cell, steps: int):
    radar = []
    if steps == 0:
        radar.append(origin)
    else:
        cell = origin.neighbor(ShipAction.NORTH.to_point() * steps)
        for _ in range(steps):
            cell = cell.neighbor(ShipAction.EAST.to_point() + ShipAction.SOUTH.to_point())
            radar.append(cell)
        for _ in range(steps):
            cell = cell.neighbor(ShipAction.WEST.to_point() + ShipAction.SOUTH.to_point())
            radar.append(cell)
        for _ in range(steps):
            cell = cell.neighbor(ShipAction.WEST.to_point() + ShipAction.NORTH.to_point())
            radar.append(cell)
        for _ in range(steps):
            cell = cell.neighbor(ShipAction.EAST.to_point() + ShipAction.NORTH.to_point())
            radar.append(cell)

    return radar


def cell_radar(origin: Cell, radius: int):
    radar = []
    for r in range(radius):
        radar.append(cell_radar_radius(origin, radius))
    return radar


# INPUTS:
# array of ship radar halite
# radar enemy ship
# radar friendly ship


def simple_agent(observation, configuration):
    """a basic agent for testing"""
    board = Board(observation, configuration)
    me = board.current_player
    turn = board.step
    halite = me.halite

    ships = me.ships
    yards = me.shipyards

    # if turn 1 build a shipyard
    if turn == 0:
        me.ships[0].next_action = ShipAction.CONVERT

    # build ships constantly unless depositing until turn 80-100ish
    spawn_cutoff = 100
    if 0 < turn < spawn_cutoff and halite >= 500 and len(yards) > 0:
        yard = yards[0]
        if yard.cell.ship is None:
            yard.next_action = ShipyardAction.SPAWN

    # move ships around as agents
    for ship in ships:
        # get vision inputs
        inputs = []
        # run inputs through specific NN
        outputs = nn_run(inputs)
        action = calc_action(outputs)
        ship.next_action = action
        # note ships may collide


def calc_action(outputs):
    """returns the desired action given NN output"""
    actions = [ShipAction.NORTH,
               ShipAction.EAST,
               ShipAction.SOUTH,
               ShipAction.WEST,
               ShipAction.CONVERT,
               None]
    i = np.array(outputs).argmax()
    return actions[i]


def nn_run(inputs):
    pass
