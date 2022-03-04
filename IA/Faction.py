
class Faction:

    def __init__(self, frac_id, heuristics=None):
        # starts at 0
        self.id = frac_id
        # diccionario id: index
        self.soldiers_dic_ids = {}
        self.soldiers = []
        self.played_turns = []
        # dic soldier id: dic soldier stat: value
        self.soldiers_stats = {}

        self.heuristic = heuristics

    def add_soldiers(self, soldiers_list):

        for item in soldiers_list:
            self.soldiers.append(item)
            self.soldiers_dic_ids[item.id] = len(self.soldiers) - 1
            self.played_turns.append(False)
            self.soldiers_stats[item.id] = {'kills': 0,
                                            'shots': 0,
                                            'shots landed': 0,
                                            'shots missed': 0,
                                            'precision avg': 0,
                                            'distance traveled': 0}

    def update_stats(self, soldier, stats):

        for ch in stats:
            self.soldiers_stats[soldier.id][ch[0]] += ch[1]
