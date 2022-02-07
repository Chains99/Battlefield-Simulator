class SimulationState:

    def __init__(self):
        """
         list of variable tuples sort by soldier id :
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
        self.team_variables = {}

        """
        dictionary team_id : moved soldiers amount
        """
        self.team_variables_moved = {}

        """
        dictionary soldier id: dictionary weapon name : ammo
        tuples values:
        soldier ammo for each weapon sort by soldier.weapons order
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
        st.team_variables = self._copy_dic(self.team_variables)
        st.team_variables_moved = self._copy_dic(self.team_variables_moved)
        st.soldier_variables = self._copy_dic(self.soldier_variables)
        st.soldier_str_variables = self._copy_dic(self.soldier_str_variables)


        st.soldier_ammo_per_weapon = self._copy_doble_dic(self.soldier_ammo_per_weapon)
        st.soldier_weapons = self._copy_doble_dic(self.soldier_weapons)
        st.soldier_weapons_current_ammo = self._copy_doble_dic(self.soldier_weapons_current_ammo)
        st.soldier_moved = self._copy_doble_dic(self.soldier_moved)
        st.soldier_died = self._copy_doble_dic(self.soldier_died)
        return st

