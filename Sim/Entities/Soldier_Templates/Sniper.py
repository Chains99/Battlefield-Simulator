from sim.Entities import Soldier


class Sniper(Soldier):

    def __init__(self, id=0, health=10, vision_range=1000, precision=0.9, move_speed=8, crit_chance=0.3, orientation='north', stance='standing', max_load=30, concealment=0.5, team=0):

        Soldier.__init__(self, id, health, vision_range, precision, move_speed, crit_chance, orientation, stance, max_load, concealment, team)
        self.w_affinities['sniper rifle'] = 1.3

