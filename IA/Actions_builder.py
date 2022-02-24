from IA.Action_manager import ActionManager
from sim.A_star.A_star import euclidean_distance
from IA.Faction import Faction
from Sim.Entities.Utilities import Sight


class ActionBuilder:

    def __init__(self, weather, sim_map):
        self.am = ActionManager(weather, sim_map)

    def _melee_attack_actions(self, soldier, state):

        position = state.soldier_positions[soldier.id]
        enemies_pos = self.am.detect_enemies(soldier, state)
        in_range = []

        for enemy_pos in enemies_pos:
            if 1 <= euclidean_distance(position, enemy_pos) <= 2:
                in_range.append(enemy_pos)

        # BUILD ACTIONS:
        # list of tuples
        # tuples: (action function, list of params)
        actions = []

        for enemy_pos in in_range:
            # CHECK IF DEAD
            enemy = state.reverse_soldier_positions[enemy_pos]
            if not state.soldier_died[enemy.team][enemy.id]:
                actions.append((self.am.melee_attack, [soldier, enemy_pos, state]))

        return actions

    def _shoot_actions(self, soldier, state):

        position = state.soldier_positions[soldier.id]
        enemies_pos = self.am.detect_enemies(soldier, state)
        in_range = []
        weapon_name = state.soldier_str_variables[soldier.id][2]
        weapon_max_range = 0

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_max_range = item.w_max_range

        for enemy_pos in enemies_pos:

            if euclidean_distance(position, enemy_pos) <= weapon_max_range:
                in_range.append(enemy_pos)

        # BUILD ACTIONS:
        # list of tuples
        # tuples: (action function, list of params)
        actions = []

        if state.soldier_variables[soldier.id][5] == 0:
            return actions

        for enemy_pos in in_range:
            # CHECK IF DEAD
            enemy = state.reverse_soldier_positions[enemy_pos]
            if not state.soldier_died[enemy.team][enemy.id]:
                actions.append((self.am.shoot_enemy, [soldier, enemy_pos, state]))

        return actions

    def _move_actions(self, soldier, state):

        actions = []
        if state.soldier_str_variables[soldier.id][0] == 'lying':
            return actions

        position = state.soldier_positions[soldier.id]
        enemies_pos = self.am.detect_enemies(soldier, state)
        out_range = []

        weapon_name = state.soldier_str_variables[soldier.id][2]
        weapon_eff_range = 0

        for item in soldier.weapons:
            if item.name == weapon_name:
                weapon_eff_range = item.w_effective_range

        for enemy_pos in enemies_pos:

            if euclidean_distance(position, enemy_pos) > weapon_eff_range:
                out_range.append(enemy_pos)

        # MOVE TOWARDS ENEMIES IN SIGHT
        # outside weapon effective range

        for enemy_pos in out_range:
            actions.append((self.am.move, [soldier, enemy_pos, state]))

        map_center = int(len(self.am.map.terrain_matrix)/2), int(len(self.am.map.terrain_matrix[0])/2)
        actions.append((self.am.move, [soldier, map_center, state]))

        return actions

    def _hide_actions(self, soldier, state):

        objects_in_sight = soldier.detect_object(state.soldier_positions[soldier.id], self.am.map.terrain_matrix)
        squares = Sight.squares_within_range(state.soldier_positions[soldier.id], soldier.vision_range, self.am.map.terrain_matrix, 'all')

        actions = []
        for item in objects_in_sight:
            actions.append((self.am.move, [soldier, item, state]))

        highest_camouflage_square = (0, (state.soldier_positions[soldier.id]))
        for item in squares:
            if self.am.map.terrain_matrix[item[0]][item[1]].camouflage > highest_camouflage_square[0]:
                highest_camouflage_square = (self.am.map.terrain_matrix[item[0]][item[1]].camouflage, item)

        if highest_camouflage_square[0] != \
                self.am.map.terrain_matrix[state.soldier_positions[soldier.id][0]][state.soldier_positions[soldier.id][1]].camouflage:
            actions.append((self.am.move, [soldier, highest_camouflage_square[1], state]))

        return actions

    def _change_stance_actions(self, soldier, state):

        stances = ['standing', 'crouching', 'lying']
        actions = []

        for i in range(len(stances)):
            if state.soldier_str_variables[soldier.id][0] != stances[i]:
                actions.append((self.am.change_stance, [soldier, stances[i], state]))

        return actions

    def _reload_action(self, soldier, state):

        actions = []

        weapon_name = state.soldier_str_variables[soldier.id][2]
        current_ammo = state.soldier_variables[soldier.id][5]
        cap_ammo = state.soldier_variables[soldier.id][6]

        if current_ammo < cap_ammo:
            actions.append((self.am.reload, [soldier, state]))

        return actions

    def change_weapon_actions(self, soldier, state):

        equiped_weapon = state.soldier_str_variables[soldier.id][2]
        weapons = soldier.weapons

        actions = []

        for item in weapons:
            if item.name != equiped_weapon:
                actions.append((self.am.change_weapon, [soldier, item.name, state]))

        return actions

    def all_soldier_actions(self, soldier, state):

        actions = []
        if state.soldier_moved[soldier.team][soldier.id] or state.soldier_died[soldier.team][soldier.id]:
            return actions
        actions.extend(self._melee_attack_actions(soldier, state))
        actions.extend(self._shoot_actions(soldier, state))
        actions.extend(self._hide_actions(soldier, state))
        actions.extend(self._move_actions(soldier, state))
        actions.extend(self._reload_action(soldier, state))
        actions.extend(self.change_weapon_actions(soldier, state))
        actions.extend(self._change_stance_actions(soldier, state))

        return actions

    def all_fraction_actions(self, fraction, state):

        soldiers = fraction.soldiers
        all_possible_actions = []

        for soldier in soldiers:
            if not state.soldier_moved[fraction.id][soldier.id] and not state.soldier_died[fraction.id][soldier.id]:
                all_possible_actions.extend(self.all_soldier_actions(soldier, state))

        if len(all_possible_actions) == 0:
            all_possible_actions.append((self.am.empty_action, [state]))

        return all_possible_actions

