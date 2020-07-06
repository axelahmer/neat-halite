# from kaggle_environments.envs.halite.helpers import *


class Ship(object):
    def __init__(self, ship_id):
        self._id = ship_id

    @property
    def id(self):
        return self._id

