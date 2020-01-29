from IdeaSim import Simulation, Event


# todo add mapping
class Manager:
    def __init__(self, simulation):
        assert isinstance(simulation, Simulation.Simulation)
        self.sim = simulation

    def manage(self, event):
        assert isinstance(event, Event.Event)
        self.sim.logger.log(str(event))

