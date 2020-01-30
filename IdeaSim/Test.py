from IdeaSim.Actions import ActionsGraph, Action, Block, Free
from IdeaSim.Event import Event
from IdeaSim.Manager import Manager
from IdeaSim.Resources import Performer
from IdeaSim.Simulation import Simulation


def test(event):
    if event.sim.now % 120 != 0:
        event.sim.manager.activate()
        raise Manager.RetryLater
    event.sim.logger.log(str(event))
    g = ActionsGraph(event.sim)
    b = Block(g, 0)
    a = Action(g, "test", 0, None, [b.id])
    Free(g, 0, None, [a.id])
    return g


def prova(action, sim, taken_inf):
    assert isinstance(sim, Simulation)
    yield sim.wait(100)
    sim.logger.log("prova")


if __name__ == '__main__':
    sim = Simulation()
    sim.manager.add_mapping("prova", test)
    Event(sim, 100, "prova")
    p = Performer(sim)
    p.add_mapping("test", prova)
    sim.add_res(p)
    sim.run()
