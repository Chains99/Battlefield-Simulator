from IA.Actions_builder import ActionBuilder
from IA.Action_manager import ActionManager
from IA.Faction import Faction
from math import inf


def min_value(simulation, fraction_eval,fraction_turn, state, depth, action_name):
    if simulation.is_terminal(state, depth):
        return simulation.evaluate_state(state, fraction_eval), None

    value = inf
    move = None
    actions = simulation.fraction_actions(fraction_turn, state)
    for action in actions:
        value2, action2 = max_value(simulation, fraction_eval,simulation.next_turn(), simulation.result(action, fraction_turn, state), depth+1, action[0])
        if value2 < value:

            value, move = value2, action

    return value, move


def max_value(simulation, fraction_eval, fraction_turn, state, depth, action_name):
    if simulation.is_terminal(state, depth):
        return simulation.evaluate_state(state, fraction_eval), None

    value = -inf
    move = None
    actions = simulation.fraction_actions(fraction_turn, state)
    for action in actions:
        value2, action2 = min_value(simulation, fraction_eval, simulation.next_turn(), simulation.result(action, fraction_turn, state), depth+1, action[0])
        if value2 > value:

            value, move = value2, action

    return value, move


def minmax_search(simulation, state):
    fraction_turn = simulation.next_turn()
    value, move = max_value(simulation, fraction_turn, fraction_turn, state, 0, None)
    return move
