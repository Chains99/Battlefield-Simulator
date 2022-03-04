from IA.Faction import Faction
from Sim.Entities.Soldier import Soldier
from typing import Dict, List


class FactionBuilder:
    def __init__(self):
        self.factions = {}

    def build_factions(self, soldiers: List[Soldier]):
        for soldier in soldiers:
            faction = self.factions.get(soldier.team)
            if faction is None:
                faction = Faction(soldier.team)
                self.factions[soldier.team] = faction
            faction.add_soldiers([soldier])

    def get_factions(self):
        return [*self.factions.values()]

