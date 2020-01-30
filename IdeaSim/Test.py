from IdeaSim.Event import Event
from IdeaSim.Simulation import Simulation


def test(event):
    event.sim.logger.log(str(event))
    Event(event.sim, event.sim.now + 1, "prova")

if __name__ == '__main__':
    sim = Simulation()
    sim.manager.add_mapping("prova", test)
    Event(sim, 100, "prova")

    sim.run()
