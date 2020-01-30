from enum import Enum

import simpy

from IdeaSim.Manager import Manager
from IdeaSim.Resources import Resources, Resource


class Simulation(simpy.Environment):
    class Logger:
        def __init__(self, env):
            self.env = env
            self.enabled = True

        class Type(Enum):
            NORMAL = ""
            HEADER = '\033[95m'
            BLUE = '\033[94m'
            WARNING = '\033[93m'
            GREEN = '\033[92m'
            FAIL = '\033[91m'
            UNDERLINE = '\033[4m'

        def enable(self, value):
            self.enabled = value

        def log(self, msg, indent=0, type=Type.NORMAL):
            if not self.enabled:
                return
            s = str(self.env.now) + ":" + " " * indent + msg
            print(type.value + s + '\033[0m')

    def __init__(self):
        super().__init__()
        self.logger = Simulation.Logger(self)

        self.manager = Manager(self)

        self.free_res = Resources(self)
        self.all_res = []

    # adding new not re-putting
    def add_res(self, res):
        assert isinstance(res, Resource)
        self.all_res.append(res)
        self.free_res.items.append(res)

    def find_res_by_id(self, id, free=True):
        l = self.free_res.items if free else self.all_res
        return list(filter(lambda x: x.id == id, l))[0]

    def find_res(self, func, free=True) -> list:
        l = self.free_res.items if free else self.all_res
        return list(filter(lambda x: func(x), l))

    def get_res_by_id(self, id):
        return self.free_res.get(lambda x: x.id == id)

    def get_res(self, func):
        return self.free_res.get(lambda x: func(x) == id)

    def put_res(self, res):
        assert isinstance(res, Resource)
        return self.free_res.put(res)

    def wait(self, delay):
        return self.timeout(delay)
