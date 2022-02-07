from IA.Actions_builder import ActionBuilder
from IA.Faction import Faction
from IA.State import SimulationState


"""
enemies_in_sight = state.soldier_variables[soldier.id][0]
                allies_in_range = state.soldier_variables[soldier.id][1]
                enemies_in_effective_range = state.soldier_variables[soldier.id][2]
                enemies_in_range = state.soldier_variables[soldier.id][3]
                fire_rate = state.soldier_variables[soldier.id][4]
                current_ammo = state.soldier_variables[soldier.id][5]
                max_ammo = state.soldier_variables[soldier.id][6]
                eff_damage = state.soldier_variables[soldier.id][7]
                damage = state.soldier_variables[soldier.id][8]
                concealment = state.soldier_variables[soldier.id][9]
                remaining_health = state.soldier_variables[soldier.id][10]
                precision = state.soldier_variables[soldier.id][11]
"""


class HeuristicManager:

    def __init__(self,
                 damage_hvalue=0.5,
                 allies_hvalue=1,
                 enemies_in_sight_hvalue=1,
                 enemies_in_range_hvalue=1,
                 low_ammo_hvalue=0.5,
                 concealment_hvalue=1,
                 remaining_hvalue=2,
                 dead_hvalue=30,
                 damage_dealt_hvalue=2):

        self.damage_hvalue = damage_hvalue
        self.allies_hvalue = allies_hvalue
        self.enemies_in_sight_hvalue = enemies_in_sight_hvalue
        self.enemies_in_range_hvalue = enemies_in_range_hvalue
        self.low_ammo_hvalue = low_ammo_hvalue
        self.concealment_hvalue = concealment_hvalue
        self.remaining_hvalue = remaining_hvalue
        self.dead_soldier_hvalue = dead_hvalue
        self.damage_dealt_hvalue = damage_dealt_hvalue

    def evaluate_state(self, state, fraction_turn, fractions):
        state_hvalue = 0
        state_hvalue += self._evaluate_soldiers_damage(state, fraction_turn)
        state_hvalue += self._nearby_soldiers_hvalue(state, fraction_turn)
        state_hvalue += self._evaluate_soldier_survival_chance(state, fraction_turn)
        state_hvalue += self._evaluate_damage_dealt(state, fraction_turn, fractions)

        return state_hvalue

    def _evaluate_damage_dealt(self, state, fraction_turn, fractions):
        total_hvalue = 0
        frac_keys = [*state.team_variables.keys()]
        # amount of dead soldiers
        for item in frac_keys:
            if item != fraction_turn.id:
                total_hvalue += (len(fractions[item].soldiers) - state.team_variables[item]) * self.dead_soldier_hvalue

        # amount of lost health
        for frac in fractions:
            if frac.id != fraction_turn.id:
                for sold in frac.soldiers:
                    total_hvalue += (sold.health - state.soldier_variables[sold.id][10]) * self.damage_dealt_hvalue

        return total_hvalue


    def _evaluate_soldiers_damage(self, state, fraction_turn):
        total_hvalue = 0

        for soldier in fraction_turn.soldiers:
            enemies_in_effective_range = state.soldier_variables[soldier.id][2]
            enemies_in_range = state.soldier_variables[soldier.id][3]
            eff_damage = state.soldier_variables[soldier.id][7]
            damage = state.soldier_variables[soldier.id][8]
            fire_rate = state.soldier_variables[soldier.id][4]
            current_ammo = state.soldier_variables[soldier.id][5]

            if current_ammo < fire_rate:
                total_hvalue -= self.low_ammo_hvalue

            if enemies_in_effective_range > 0:
                total_hvalue += eff_damage * self.damage_hvalue
                continue
            if enemies_in_range > 0:
                total_hvalue += damage * self.damage_hvalue

        return total_hvalue

    def _nearby_soldiers_hvalue(self, state, fraction_turn):
        total_hvalue = 0

        for soldier in fraction_turn.soldiers:
            enemies_in_sight = state.soldier_variables[soldier.id][0]
            allies_in_range = state.soldier_variables[soldier.id][1]
            enemies_in_effective_range = state.soldier_variables[soldier.id][2]
            enemies_in_range = state.soldier_variables[soldier.id][3]

            total_hvalue += allies_in_range * self.allies_hvalue
            total_hvalue += enemies_in_effective_range * self.enemies_in_range_hvalue
            total_hvalue += (enemies_in_range * self.enemies_in_range_hvalue)/2
            total_hvalue -= enemies_in_sight * self.enemies_in_sight_hvalue

        return total_hvalue

    def _evaluate_soldier_survival_chance(self, state, fraction_turn):
        total_hvalue = 0

        for soldier in fraction_turn.soldiers:
            concealment = state.soldier_variables[soldier.id][9]
            remaining_health = state.soldier_variables[soldier.id][10]

            total_hvalue += concealment * self.concealment_hvalue
            if remaining_health > 0:
                total_hvalue += remaining_health * self.remaining_hvalue
            else:
                total_hvalue -= self.dead_soldier_hvalue

        return total_hvalue


# add non_terminal finish conditions
class SimulationManager:

    def __init__(self, fractions_list, weather, sim_map, heuristics, max_depth):
        self.fractions = fractions_list
        self.current_turn = 0
        self.ab = ActionBuilder(weather, sim_map)
        self.heuristic = heuristics
        self.max_depth = max_depth

    def next_turn(self):
        fraction_turn = self.fractions[self.current_turn]
        self.current_turn += 1
        if self.current_turn == len(self.fractions):
            self.current_turn = 0
        return fraction_turn

    def fraction_actions(self, fraction, state):
        return self.ab.all_fraction_actions(fraction, state)

    def evaluate_state(self, state, fraction):
        return self.heuristic.evaluate_state(state, fraction, self.fractions)

    def is_terminal(self, state, depth):
        if depth >= self.max_depth:
            return True

        for item in self.fractions:
            if state.team_variables[item.id] == 0:
                return True

        return False

    def build_initial_state(self, fractions, action_manager, soldier_positions):

        state = SimulationState()

        # positions
        for sol_pos in soldier_positions:
            state.soldier_positions[sol_pos[0].id] = sol_pos[1]
            state.reverse_soldier_positions[sol_pos[1]] = sol_pos[0]
            state.soldiers_in_map[sol_pos[0].id] = sol_pos[0]

        for fraction in fractions:

            state.team_variables[fraction.id] = len(fraction.soldiers)
            state.team_variables_moved[fraction.id] = 0
            state.soldier_moved[fraction.id] = {}
            state.soldier_died[fraction.id] = {}

            for soldier in fraction.soldiers:

                # soldier string variables
                soldier.detect_object(state.soldier_positions[soldier.id], action_manager.map.terrain_matrix)
                stance = soldier.stance
                if soldier.next_to_object:
                    next_object = 'T'
                else:
                    next_object = 'F'
                equipped_w_name = soldier.equipped_weapon.name

                state.soldier_str_variables[soldier.id] = (stance, next_object, equipped_w_name)

                # Soldier_Templates variables
                enemies_in_sight = action_manager.detect_enemies(soldier, state)
                allies_in_range = action_manager.detect_allies(soldier, state)
                enemies_in_range = action_manager.amount_enemies_in_effective_range(soldier, enemies_in_sight, state)
                enemies_in_max_range = action_manager.amount_enemies_out_of_effective_range(soldier, enemies_in_sight, state)
                fire_rate = soldier.equipped_weapon.fire_rate
                current_ammo = soldier.equipped_weapon.current_ammo
                max_ammo = soldier.equipped_weapon.ammunition_capacity
                weapon_damage_raw = soldier.equipped_weapon.damage
                weapon_eff_damage = 0
                weapon_damage = 0
                concealment = soldier.concealment
                remaining_health = soldier.health
                precision = soldier.precision

                weapon_aff = soldier.w_affinities[equipped_w_name]
                weapon_eff_damage = weapon_damage_raw * fire_rate * weapon_aff
                weapon_damage = (weapon_damage_raw * fire_rate * weapon_aff)/2

                state.soldier_variables[soldier.id] = (len(enemies_in_sight),
                                                       len(allies_in_range),
                                                       enemies_in_range,
                                                       enemies_in_max_range,
                                                       fire_rate,
                                                       current_ammo,
                                                       max_ammo,
                                                       weapon_eff_damage,
                                                       weapon_damage,
                                                       concealment,
                                                       remaining_health,
                                                       precision)

                state.soldier_moved[fraction.id][soldier.id] = False
                state.soldier_died[fraction.id][soldier.id] = False

                # weapon state variables
                state.soldier_weapons[soldier.id] = {}
                state.soldier_ammo_per_weapon[soldier.id] = {}
                state.soldier_weapons_current_ammo[soldier.id] = {}

                for weapon in soldier.weapons:

                    state.soldier_weapons[soldier.id][weapon.name] = weapon
                    state.soldier_ammo_per_weapon[soldier.id][weapon.name] = soldier.weapon_ammo[weapon.name]
                    state.soldier_weapons_current_ammo[soldier.id][weapon.name] = weapon.current_ammo

        return state

    def is_soldier_available(self, fraction, soldier, state):
        if state.soldier_moved[fraction.id][soldier.id]:
            return False
        if state.soldier_died[fraction.id][soldier.id]:
            return False
        return True

    def result(self, action, fraction, state):

        result_state = action[0](*action[1])

        soldier = action[1][0]
        result_state.team_variables_moved[fraction.id] += 1
        result_state.soldier_moved[soldier.team][soldier.id] = True

        # count alive soldiers
        for item in [*result_state.soldier_variables.keys()]:
            # if soldier dead
            if result_state.soldier_variables[item][10] <= 0:
                sold_inst = result_state.soldiers_in_map[item]
                if not result_state.soldier_died[sold_inst.team][sold_inst.id]:
                    # then sold_inst is dead
                    result_state.soldier_died[sold_inst.team][sold_inst.id] = True
                    result_state.team_variables[sold_inst.team] -= 1

        if self.needed_reset(result_state):
            result_state = self.reset_moves(result_state)

        return result_state

    def reset_moves(self, state):

        for fraction in self.fractions:
            state.team_variables_moved[fraction.id] = 0
            for soldier in fraction.soldiers:
                state.soldier_moved[fraction.id][soldier.id] = False

        return state

    def needed_reset(self, state):

        for fraction in self.fractions:
            if state.team_variables_moved[fraction.id] != len(fraction.soldiers):
                return False

        return True
