from sim.Entities import Soldier


class Scout(Soldier):

    def __init__(self, id=0, health=10, vision_range=600, precision=0.6, move_speed=17, crit_chance=0.3, orientation='north', stance='standing', max_load=30, concealment=0.2, team=0):

        Soldier.__init__(self, id, health, vision_range, precision, move_speed, crit_chance, orientation, stance, max_load, concealment, team)
