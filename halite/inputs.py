from kaggle_environments.envs.halite.helpers import *

# file for determining NN inputs

def get_radar_cell_array(cell: Cell, radius: int):
    offset = Point(0, 0)
    radar = []
    x = 0
    y = 0
    for r in range(radius):
        cells = []

        radar.append(cells)
    cell.neighbor(Point(1,1))
# INPUTS:
# array of ship radar halite
# radar enemy ship
# radar friendly ship


def agent(observation, configuration):
    """a basic agent for testing"""
    board = Board(observation, configuration)
    cp = board.current_player

    ships = cp.ships
    yards = cp.shipyards






