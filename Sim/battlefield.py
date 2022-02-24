from IA.MinMax import minmax_search


class BattleField:

    def __init__(self, simulation,  console=None):
        self.sim = simulation
        self.fractions = simulation.fractions
        self.finish = False
        self.started = False
        self.current_state = None
        self.console = console

    def run_battlefield(self, soldier_pos):

        if not self.started:
            self.current_state = self.sim.build_initial_state(self.sim.fractions, self.sim.ab.am, soldier_pos)
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
            self.console.print('soldier id:{} team:{} attacked soldier id:{} team:{}'.format(move[1][0].id, move[1][0].team, enemy.id, enemy.team))

        if move[0] == self.sim.ab.am.shoot_enemy:
            enemy = self.current_state.reverse_soldier_positions[move[1][1]]
            self.console.print('soldier id:{} team:{} shoot soldier id:{} team:{}'.format(move[1][0].id, move[1][0].team, enemy.id, enemy.team))

        if move[0] == self.sim.ab.am.move:
            self.console.print('soldier id:{} team:{} moved towards square {}'.format(move[1][0].id, move[1][0].team, self.current_state.soldier_positions[move[1][0].id]))

        if move[0] == self.sim.ab.am.change_stance:
            self.console.print('soldier id:{} team:{} changed stance to {}'.format(move[1][0].id, move[1][0].team, move[1][0].stance))

        if move[0] == self.sim.ab.am.reload:
            self.console.print('soldier id:{} team:{} reloaded'.format(move[1][0].id, move[1][0].team))

        if move[0] == self.sim.ab.am.change_weapon:
            self.console.print('soldier id:{} change weapon to {}'.format(move[1][0].id, move[1][0].team, move[1][0].equipped_weapon.name))

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

        if self.needed_reset(result_state):
            result_state = self.reset_moves(result_state)

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

