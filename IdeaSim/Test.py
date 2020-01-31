from IdeaSim.Actions import ActionsGraph, Action, Block, Free, GenerateEvent
from IdeaSim.Event import Event
from IdeaSim.Manager import Manager
from IdeaSim.Resources import Performer, Resource
from IdeaSim.Simulation import Simulation


def test(event):
    if event.sim.now % 120 != 0:
        event.sim.manager.activate()
        raise Manager.RetryLater
    event.sim.logger.log(str(event))
    g = ActionsGraph(event.sim)
    b = Block(g, lambda x: True, )
    a = Action(g, "test", lambda x: True, param=None, after=[b.id])
    Free(g, lambda x: True, None, param=[a.id])
    return g


class Well(Resource):

    def __init__(self, sim):
        super().__init__(sim)


class Tank(Resource):

    def __init__(self, sim):
        super().__init__(sim)


class Aquifer(Performer):

    def __init__(self, sim):
        super().__init__(sim)
        self.add_mapping("take", self.take)
        self.add_mapping("drop", self.drop)
        Event(sim, 10 + len(sim.all_res), "haul")

    def take(self, action, sim, taken_inf):
        yield sim.wait(10)

    def drop(self, action, sim, taken_inf):
        yield sim.wait(10)


class Status:
    def __init__(self, sim):
        self.rain = False
        self.sim = sim
        sim.manager.add_mapping("weather", Status.change_of_whether)
        Event(sim, 50, "weather")

    def toggle_rain(self):
        self.rain = not self.rain
        self.sim.logger.log("Rain " + str(self.rain), 6)

    @staticmethod
    def change_of_whether(event):
        event.sim.modify_status().toggle_rain()
        Event(sim, sim.now + 50, "weather")


def haul(event):
    if event.sim.get_status().rain:
        raise Manager.RetryLater()
    g = ActionsGraph(event.sim)
    b = Block(g, lambda x: isinstance(x, Aquifer))
    b1 = Block(g, lambda x: isinstance(x, Well))
    t = Action(g, "take", lambda x: isinstance(x, Aquifer), param={"well": lambda x: isinstance(x, Well)},
               after=[b.id, b1.id])
    f1 = Free(g, lambda x: isinstance(x, Well), None, after=[t.id])
    b1 = Block(g, lambda x: isinstance(x, Tank), after=[t.id])
    t = Action(g, "drop", lambda x: isinstance(x, Aquifer), param={"tank": lambda x: isinstance(x, Tank)},
               after=[b1.id])
    f = Free(g, lambda x: isinstance(x, Aquifer), None, after=[t.id])
    f1 = Free(g, lambda x: isinstance(x, Tank), None, after=[t.id])
    GenerateEvent(g, Event(sim, None, "haul"), after=[f1.id, f.id])
    return g


if __name__ == '__main__':
    sim = Simulation()
    sim.__status__ = Status(sim)
    sim.manager.add_mapping("haul", haul)

    sim.add_res(Well(sim))
    sim.add_res(Tank(sim))
    sim.add_res(Well(sim))
    p = Aquifer(sim)
    sim.add_res(p)
    p = Aquifer(sim)
    sim.add_res(p)
    sim.run()
