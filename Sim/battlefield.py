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

        if self.finish:

            next_move = minmax_search(self.sim, self.current_state)

            self.current_state = self.perfom_action(next_move)

            self.move_view(next_move)

            if self.terminal_state():
               return True
        return False
    def move_view(self, move):

        if move == self.sim.ab.am.shoot_enemy:
            enemy = self.current_state.reverse_soldier_positions[move[1][1]]
            self.console.print('soldier id:{} team:{} shoot soldier id:{} team:{}'.format(move[1][0].id, move[1][0].team, enemy.id, enemy.team))

        if move == self.sim.ab.am.move:
            self.console.print('soldier id:{} team:{} moved towards square {}'.format(move[1][0].id, move[1][0].team, self.current_state.soldier_positions[move[1][0].id]))

        if move == self.sim.ab.am.change_stance:
            self.console.print('soldier id:{} team:{} changed stance to {}'.format(move[1][0].id, move[1][0].team, move[1][0].stance))

        if move == self.sim.ab.am.reload:
            self.console.print('soldier id:{} team:{} reloaded'.format(move[1][0].id, move[1][0].team))

        if move == self.sim.ab.am.change_weapon:
            self.console.print('soldier id:{} change weapon to {}'.format(move[1][0].id, move[1][0].team, move[1][0].equipped_weapon.name))

    def terminal_state(self):

        for item in self.fractions:
            if self.current_state.team_variables[item.id] == 0:
                return True
        return False

    def perfom_action(self, action):

        if action[0] == self.sim.ab.am.shoot_enemy:
            return self.sim.ab.am.real_shoot_enemy(*action[1])

        if action[0] == self.sim.ab.am.move:
            return self.sim.ab.am.real_move(*action[1])

        if action[0] == self.sim.ab.am.change_stance:
            return self.sim.ab.am.real_change_stance(*action[1])

        if action[0] == self.sim.ab.am.reload:
            return self.sim.ab.am.real_reload(*action[1])

        if action[0] == self.sim.ab.am.change_weapon:
            return self.sim.ab.am.real_change_weapon(*action[1])


