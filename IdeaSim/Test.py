from IdeaSim.Event import Event
from IdeaSim.Manager import Manager
from IdeaSim.Simulation import Simulation


def test(event):

    if event.sim.now % 120 != 0:
        event.sim.manager.activate()
        raise Manager.RetryLater
    event.sim.logger.log(str(event))
    Event(event.sim, event.sim.now + 1, "prova")


if __name__ == '__main__':
    sim = Simulation()
    sim.manager.add_mapping("prova", test)
    Event(sim, 100, "prova")

    sim.run()
