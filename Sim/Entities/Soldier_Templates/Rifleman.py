from sim.Entities import Soldier


class Rifleman(Soldier):

    def __init__(self, id=0, health=25, vision_range=600, precision=0.8, move_speed=12, crit_chance=0.15, orientation='north', stance='standing', max_load=30, concealment=0.25, team=0):

        Soldier.__init__(self, id, health, vision_range, precision, move_speed, crit_chance, orientation, stance, max_load, concealment, team)
        self.w_affinities['AK 47'] = 1.3
        self.w_affinities['M16'] = 1.3
        self.w_affinities['M4'] = 1.3
        self.w_affinities['Scar'] = 1.3
