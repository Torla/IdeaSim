import itertools
from enum import Enum

from simpy import Container

from IdeaSim import Simulation
from IdeaSim.Resources import Performer


class Action:
    new_id = itertools.count()

    def __init__(self, action_graph, action_type, who, param=None, after=None):
        self.id = next(self.new_id)
        assert isinstance(action_graph, ActionsGraph)
        action_graph.actions[self.id] = self
        self.actionType = action_type
        self.who = who
        assert isinstance(param, dict) or param is None
        self.param = {} if param is None else param
        assert isinstance(after, list) or after is None
        self.after = [] if after is None else after


class Block(Action):

    def __init__(self, action_graph, who, param=None, after=None):
        super().__init__(action_graph, "Block", who, param, after)


class Free(Action):

    def __init__(self, action_graph, who, param=None, after=None):
        super().__init__(action_graph, "Free", who, param, after)


class ActionsGraph:
    def __init__(self, sim):
        assert isinstance(sim, Simulation.Simulation)
        self.sim = sim
        self.actions = {}


class Executor:
    def __init__(self, sim, action_tree):

        assert isinstance(action_tree, ActionsGraph)
        self.action_tree = action_tree
        self.sim = sim
        sim.process(self.run())

    def run(self):
        wait = None
        taken_inf = []
        completed_flags = {}

        for action_id in self.action_tree.actions.keys():
            completed_flags[action_id] = Container(self.sim)

        for action in self.action_tree.actions.values():
            self.sim.process(
                self.execute(action, taken_inf, self.sim, completed_flags))

        for flag in completed_flags.values():
            if wait is None:
                wait = flag.get(1)
            else:
                wait = wait & flag.get(1)
        yield wait

        if len(taken_inf) != 0:
            raise Exception("Resources not free at end of task")

        self.sim.manager.activate()

    def execute(self, action, taken_inf, sim, completed_flags):
        assert isinstance(action, Action)
        assert isinstance(sim, Simulation.Simulation)
        wait = None
        try:
            for action_id in action.after:
                if wait is None:
                    wait = completed_flags[action_id].get(1)
                else:
                    wait = wait & completed_flags[action_id].get(1)
            if wait is not None:
                yield wait
        except KeyError:
            sim.logger.log("waiting for non existing action", 0, sim.logger.Type.FAIL)

        if isinstance(action, Block):
            if callable(action.who):
                action.who = sim.find_res(action.who, free=False)[0].id
            yield sim.get_res_by_id(action.who)
            taken_inf.append(sim.find_res_by_id(action.who, free=False))
            yield completed_flags[action.id].put(float('inf'))
            sim.logger.log("blocking  " + str(
                sim.find_res_by_id(action.who, free=False)),
                           7)

        elif isinstance(action, Free):
            if callable(action.who):
                action.who = sim.find_res(action.who, free=False)[0].id
            inf = list(filter(lambda x: x.id == action.who, taken_inf))[0]
            yield sim.put_res(inf)
            taken_inf.remove(inf)
            yield completed_flags[action.id].put(float('inf'))
            # manager is activated after anything is free
            sim.logger.log("Free " + str(
                sim.find_res_by_id(action.who)
            ),
                           7)
            self.sim.manager.activate()

        else:
            try:
                if callable(action.who):
                    action.who = list(filter(lambda x: action.who(x), taken_inf))[0].id
                yield self.sim.process(
                    list(filter(lambda x: x.id == action.who, taken_inf))[0].perform(action, taken_inf))
            except Performer.IllegalAction as err:
                sim.logger.log(str(err), type=sim.logger.Type.FAIL)
            except KeyError as err:
                sim.logger.log("Action parameter not defined" + str(err), type=sim.logger.Type.FAIL)
            except IndexError as err:
                sim.logger.log("Performer not blocked " + str(err), type=sim.logger.Type.FAIL)

            completed_flags[action.id].put(float('inf'))
