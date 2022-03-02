class SimulationState:

    def __init__(self):
        """
         dictionary of variable tuples sort by soldier id :
         [enemies_in_sight,
          allies_in_range,
          enemies_in_effective_range,
          enemies_in_range (not effective),
          fire_rate,
          current_ammo,
          max_ammo,
          weapon_effective_damage,
          weapon_damage,
          concealment,
          remaining_health,
          precision
         ]
         """
        self.soldier_variables = {}
        """
        list of string variables tuples sort by soldier id :
        (stance,
        next_to_object,  (T: true, F: false)
        equipped_weapon_name,
        )
        """
        self.soldier_str_variables = {}

        """
        dictionary of variable tuples sort by soldier id :
        [
        vision_range,
        move_speed,
        crit_chance,
        max_load,
        melee_damage
        ]
        """
        self.soldier_extra_variables = {}
        """
        dictionary soldier id : position
        """
        self.soldier_positions = {}
        """
        dictionary position: soldier instance
        """
        self.reverse_soldier_positions = {}
        """
        dictionary id: soldier instance
        """
        self.soldiers_in_map = {}
        """
        dictionary team_id : alive soldiers
        """
        self.alive_soldiers = {}

        """
        dictionary team_id : moved soldiers amount
        """
        self.team_variables_moved = {}

        """
        dictionary soldier id: dictionary weapon name : ammo
        """
        self.soldier_ammo_per_weapon = {}
        """
        dictionary soldier id : dictionary weapon name : current ammo
        """
        self.soldier_weapons_current_ammo = {}

        """
        dictionary soldiers id : weapon name: weapon reference
        """
        self.soldier_weapons = {}
        """
        dictionary fraction id: dictionary soldier id : bool 
        """
        self.soldier_moved = {}

        """
        dictionary fraction id: dictionary soldier id : bool 
        """
        self.soldier_died = {}

        self.building = False

    def _copy_list(self, list_to_copy):
        new_list = []
        for item in list_to_copy:
            new_list.append(item)
        return new_list

    def _copy_dic(self, dic):
        new_dic = {}
        for item in [*dic.keys()]:
            new_dic[item] = dic[item]
        return new_dic

    def _copy_doble_dic(self, dic):
        new_dic = {}
        for item in [*dic.keys()]:
            new_dic[item] = {}
            for item2 in [*dic[item].keys()]:
                new_dic[item][item2] = dic[item][item2]
        return new_dic

    def copy_state(self):
        st = SimulationState()
        st.reverse_soldier_positions = self._copy_dic(self.reverse_soldier_positions)
        st.soldier_positions = self._copy_dic(self.soldier_positions)
        st.soldiers_in_map = self._copy_dic(self.soldiers_in_map)
        st.alive_soldiers = self._copy_dic(self.alive_soldiers)
        st.team_variables_moved = self._copy_dic(self.team_variables_moved)
        st.soldier_variables = self._copy_dic(self.soldier_variables)
        st.soldier_extra_variables = self._copy_dic(self.soldier_extra_variables)
        st.soldier_str_variables = self._copy_dic(self.soldier_str_variables)

        st.soldier_ammo_per_weapon = self._copy_doble_dic(self.soldier_ammo_per_weapon)
        st.soldier_weapons = self._copy_doble_dic(self.soldier_weapons)
        st.soldier_weapons_current_ammo = self._copy_doble_dic(self.soldier_weapons_current_ammo)
        st.soldier_moved = self._copy_doble_dic(self.soldier_moved)
        st.soldier_died = self._copy_doble_dic(self.soldier_died)
        return st


def build_new_state(factions, action_manager, soldier, state):
    new_state = state.copy_state()
    new_state.building = True

    for faction in factions:

        new_state.alive_soldiers[faction.id] = len(faction.soldiers)
        new_state.team_variables_moved[faction.id] = 0

        for soldier in faction.soldiers:

            new_state.soldier_positions[soldier.id] = soldier.position
            new_state.reverse_soldier_positions[soldier.position] = soldier
            new_state.soldiers_in_map[soldier.id] = soldier

            # soldier string variables
            soldier.detect_object(new_state.soldier_positions[soldier.id], action_manager.map.terrain_matrix)
            stance = soldier.stance
            if soldier.next_to_object:
                next_object = 'T'
            else:
                next_object = 'F'

            if soldier.equipped_weapon is not None:
                equipped_w_name = soldier.equipped_weapon.name
            else:
                equipped_w_name = 'None'

            new_state.soldier_str_variables[soldier.id] = (stance, next_object, equipped_w_name)

            # Soldier_Templates variables
            enemies_in_sight = action_manager.detect_enemies(soldier, new_state)
            allies_in_range = action_manager.detect_allies(soldier, new_state)
            enemies_in_range = action_manager.amount_enemies_in_effective_range(soldier, enemies_in_sight, new_state)
            enemies_in_max_range = action_manager.amount_enemies_out_of_effective_range(soldier, enemies_in_sight,
                                                                                        new_state)

            if equipped_w_name != 'None':
                fire_rate = soldier.equipped_weapon.fire_rate
                current_ammo = soldier.equipped_weapon.current_ammo
                max_ammo = soldier.equipped_weapon.ammunition_capacity
                weapon_damage_raw = soldier.equipped_weapon.damage
                weapon_aff = soldier.w_affinities[equipped_w_name]
                weapon_eff_damage = weapon_damage_raw * fire_rate * weapon_aff
                weapon_damage = (weapon_damage_raw * fire_rate * weapon_aff) / 2
            else:
                fire_rate = 0
                current_ammo = 0
                max_ammo = 0
                weapon_eff_damage = 0
                weapon_damage = 0

            concealment = soldier.concealment
            remaining_health = soldier.health
            precision = soldier.precision

            new_state.soldier_variables[soldier.id] = (len(enemies_in_sight),
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


            new_state.soldier_extra_variables[soldier.id] = (soldier.vision_range,
                                                             soldier.move_speed,
                                                             soldier.crit_chance,
                                                             soldier.max_load,
                                                             soldier.melee_damage)

            if new_state.soldier_variables[soldier.id][10] <= 0 and not new_state.soldier_died[soldier.team][soldier.id]:
                new_state.alive_soldiers[soldier.team] -= 1
                new_state.soldier_died[soldier.team][soldier.id] = True

            # weapon state variables
            for weapon in soldier.weapons:
                new_state.soldier_ammo_per_weapon[soldier.id][weapon.name] = soldier.weapon_ammo[weapon.name]
                new_state.soldier_weapons_current_ammo[soldier.id][weapon.name] = weapon.current_ammo

    new_state.soldier_moved[soldier.team][soldier.id] = True
    new_state.team_variables_moved[soldier.team] += 1

    new_state.building = False
    return new_state


def revert_general_changes(factions, old_state):

    for faction in factions:
        for soldier in faction.soldiers:

            # STR VARIABLES
            soldier.stance = old_state.soldier_str_variables[soldier.id][0]
            if old_state.soldier_str_variables[soldier.id][1] == 'T':
                soldier.next_to_object = True
            else:
                soldier.next_to_object = False

            eq_w_name = old_state.soldier_str_variables[soldier.id][2]
            if eq_w_name == 'None':
                continue
            for weapon in soldier.weapons:
                if weapon.name == eq_w_name:
                    soldier.equipped_weapon = weapon
                    break

            # NUMERIC VARIABLES
            soldier.position = old_state.soldier_positions[soldier.id]
            soldier.equipped_weapon.current_ammo = old_state.soldier_variables[soldier.id][5]
            soldier.concealment = old_state.soldier_variables[soldier.id][9]
            soldier.current_health = old_state.soldier_variables[soldier.id][10]
            soldier.precision = old_state.soldier_variables[soldier.id][11]

            soldier.vision_range = old_state.soldier_extra_variables[soldier.id][0]
            soldier.move_speed = old_state.soldier_extra_variables[soldier.id][1]
            soldier.crit_chance = old_state.soldier_extra_variables[soldier.id][2]
            soldier.max_load = old_state.soldier_extra_variables[soldier.id][3]
            soldier.melee_damage = old_state.soldier_extra_variables[soldier.id][4]

            for weapon in soldier.weapons:
                soldier.weapon_ammo[weapon.name] = old_state.soldier_ammo_per_weapon[soldier.id][weapon.name]
                weapon.current_ammo = old_state.soldier_weapons_current_ammo[soldier.id][weapon.name]

"""
def extra_action_deco(state, factions, action_manager):

    def inner_f(function):
        def inner(*args):
            # executes the actions and returns new state
            function(*args)
            return build_new_state(factions, action_manager, state)

        return inner

    return inner_f
"""

