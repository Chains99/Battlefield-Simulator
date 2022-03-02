from IA.MinMax import minmax_search
from IA.State import build_new_state
from IA.simulation import HeuristicManager, SimulationManager
from Sim.Entities.Soldier import Soldier
from Sim.Make_Factions import FactionBuilder
from Sim.aux_actions import decorate_aux_actions


class BattleField:

    def __init__(self, simulation):
        self.sim = simulation
        self.fractions = simulation.fractions
        self.finish = False
        self.started = False
        self.current_state = None

    def run_battlefield(self):

        if not self.started:
            self.current_state = self.sim.build_initial_state(self.sim.fractions, self.sim.ab.am)
            self.started = True

        # while not self.finish:
        if not self.finish:
            current_turn = self.sim.current_turn
            next_move = minmax_search(self.sim, self.current_state)

            self.current_state = self.perfom_action(next_move)

            self.sim.set_on_next_turn(current_turn)

            self.move_view(next_move)

            if self.terminal_state():
                return True

        return False

    def move_view(self, move):

        if move[0] == self.sim.ab.am.melee_attack:
            enemy = self.current_state.reverse_soldier_positions[move[1][1]]
            print('soldier id:{} team:{} attacked soldier id:{} team:{}'.format(move[1][0].id, move[1][0].team, enemy.id, enemy.team))

        if move[0] == self.sim.ab.am.shoot_enemy:
            enemy = self.current_state.reverse_soldier_positions[move[1][1]]
            print('soldier id:{} team:{} shoot soldier id:{} team:{}'.format(move[1][0].id, move[1][0].team, enemy.id, enemy.team))

        if move[0] == self.sim.ab.am.move:
            print('soldier id:{} team:{} moved towards square {}'.format(move[1][0].id, move[1][0].team, self.current_state.soldier_positions[move[1][0].id]))

        if move[0] == self.sim.ab.am.change_stance:
            print('soldier id:{} team:{} changed stance to {}'.format(move[1][0].id, move[1][0].team, move[1][0].stance))

        if move[0] == self.sim.ab.am.reload:
            print('soldier id:{} team:{} reloaded'.format(move[1][0].id, move[1][0].team))

        if move[0] == self.sim.ab.am.change_weapon:
            print('soldier id:{} change weapon to {}'.format(move[1][0].id, move[1][0].team, move[1][0].equipped_weapon.name))

    def terminal_state(self):

        for item in self.fractions:
            if self.current_state.alive_soldiers[item.id] == 0:
                return True
        return False

    def perfom_action(self, action):

        result_state = None

        if action[0] == self.sim.ab.am.melee_attack:
            result_state, stats = self.sim.ab.am.real_melee_attack(*action[1])
            self.fractions[action[1][0].team].update_stats(action[1][0], stats)

        if action[0] == self.sim.ab.am.shoot_enemy:
            result_state, stats = self.sim.ab.am.real_shoot_enemy(*action[1])
            self.fractions[action[1][0].team].update_stats(action[1][0], stats)

        if action[0] == self.sim.ab.am.move:
            result_state, stats = self.sim.ab.am.real_move(*action[1])
            self.fractions[action[1][0].team].update_stats(action[1][0], stats)

        if action[0] == self.sim.ab.am.change_stance:
            result_state = self.sim.ab.am.real_change_stance(*action[1])

        if action[0] == self.sim.ab.am.reload:
            result_state = self.sim.ab.am.real_reload(*action[1])

        if action[0] == self.sim.ab.am.change_weapon:
            result_state = self.sim.ab.am.real_change_weapon(*action[1])

        if action[0] == self.sim.ab.am.empty_action:
            result_state = self.sim.ab.am.empty_action(*action[1])
            if self.needed_reset(result_state):
                result_state = self.reset_moves(result_state)
            return result_state

        soldier = action[1][0]
        if result_state is not None:
            result_state.team_variables_moved[soldier.team] += 1
            result_state.soldier_moved[soldier.team][soldier.id] = True

        if result_state is not None:
            if self.needed_reset(result_state):
                result_state = self.reset_moves(result_state)

        if result_state is None:
            self.perform_extra_action(action)

        return result_state

    def perform_extra_action(self, action):
        """
        USE TRY
        """
        # decorate all auxiliary function to current state
        decorate_aux_actions(action[2])
        # execute extra action
        action[0](action[1], self.sim.sim_map.terrain_matrix)
        # generate new state
        result_state = build_new_state(self.fractions, self.sim.ab.am, action[2])
        return result_state

    def needed_reset(self, state):

        for fraction in self.fractions:
            if state.team_variables_moved[fraction.id] != state.alive_soldiers[fraction.id]:
                return False

        return True

    def reset_moves(self, state):

        for fraction in self.fractions:
            state.team_variables_moved[fraction.id] = 0
            for soldier in fraction.soldiers:
                state.soldier_moved[fraction.id][soldier.id] = False

        return state


def build_battlefield(sim_map, weather, soldiers, max_depth, heuristics=[]):

    # CHECK SOLDIERS INSTANCES
    for soldier in soldiers:
        if not isinstance(soldier, Soldier):
            raise Exception('Invalid element in soldiers')
    # CHECK IF NO HEURISTICS
    if len(heuristics) == 0:
        heur = HeuristicManager()
        heuristics = [heur, heur]
    # CHECK DEPTH
    if max_depth < 1:
        raise Exception('Invalid max_depth value')

    fb = FactionBuilder()
    fb.build_factions(soldiers)
    fb.factions[0].heuristic = heuristics[0]
    fb.factions[1].heuristic = heuristics[1]
    sim = SimulationManager(fb.get_factions(), weather, sim_map=sim_map, max_depth=max_depth)

    return BattleField(sim)
