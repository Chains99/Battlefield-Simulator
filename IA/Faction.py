
class Faction:

    def __init__(self, frac_id):
        # starts at 0
        self.id = frac_id
        # diccionario id: index
        self.soldiers_dic_ids = {}
        # dic de soldados (soldier id: (soldier
        self.soldiers = []
        self.played_turns = []

    def add_soldiers(self, soldiers_list):

        for item in soldiers_list:
            self.soldiers.append(item)
            self.soldiers_dic_ids[item.id] = len(self.soldiers) - 1
            self.played_turns.append(False)

