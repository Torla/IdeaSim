import itertools

from simpy import FilterStore

from IdeaSim import Simulation


class Resources(FilterStore):
    def __init__(self, env, capacity=float('inf')):
        super().__init__(env, capacity)


class Resource:
    new_id = itertools.count()

    def __init__(self, sim):
        assert isinstance(sim, Simulation.Simulation)
        self.sim = sim
        self.id = next(self.new_id)


class Performer(Resource):
    def __init__(self, sim):
        super().__init__(sim)
        self.action_map = {}

    class IllegalAction(Exception):
        def __init__(self, msg):
            self.msg = msg

    def perform(self, action):
        self.action_map[action.actionType](action)
