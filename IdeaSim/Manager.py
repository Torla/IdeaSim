from IdeaSim import Simulation, Event


# todo add mapping
class Manager:
    def __init__(self, simulation):
        assert isinstance(simulation, Simulation.Simulation)
        self.sim = simulation
        self.type_map = {}

    def add_mapping(self, event_type, func):
        self.type_map[event_type] = func

    def manage(self, event):
        assert isinstance(event, Event.Event)
        self.type_map[event.event_type](event)
