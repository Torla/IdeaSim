# to be implemented by the and user
from IdeaSim.Simulation import Simulation


class Event:
    def __init__(self, sim, time, event_type):
        assert isinstance(sim, Simulation)
        self.sim = sim
        self.time = time
        self.event_type = event_type
        self.sim.process(self.__dispatch__())

    def __dispatch__(self):
        yield self.sim.wait(self.time - self.sim.now)
        self.sim.manager.manage(self)
