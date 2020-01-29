from IdeaSim.Event import Event
from IdeaSim.Simulation import Simulation

if __name__ == '__main__':
    sim = Simulation()
    Event(sim, 100, "prova")
    Event(sim, 1100, "prova")
    Event(sim, 1200, "prova")
    sim.run()
