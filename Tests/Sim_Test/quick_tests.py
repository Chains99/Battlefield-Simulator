from Sim.Entities.Soldier import Soldier
from Sim.Entities.Weapon import Weapon, default_weapons
from Sim.Entities.Map import Map
from Sim.Entities.Weather import Weather
from Sim.Entities.Weapon import Weapon
from IA.Faction import Faction
from IA.simulation import SimulationManager
from IA.simulation import HeuristicManager
from Sim.battlefield import BattleField
from Sim.Make_Factions import FactionBuilder
from IA.MinMax import minmax_search
from Sim.A_star.A_star import euclidean_distance
from math import inf
from IA.State import SimulationState
from IA.Action_manager import ActionManager
from IA.Actions_builder import ActionBuilder


def run_test(output_dest):
    """
    State and Map, weather
    """
    mapa = Map(5, 5)
    weather = Weather(0, 0, 0, 0, 0, 0)

    """
    Soldiers
    params:
    
    id,
    health,
    vision_range,
    precision,
    move_speed,
    crit_chance,
    orientation,
    stance,
    max_load,
    concealment,
    team
    """
    s1 = Soldier(10, 10, 0.5, 6, 0, 'north', 'standing', 10, 0.2, 0)
    s2 = Soldier(10, 10, 0.5, 2, 0, 'north', 'standing', 10, 0.2, 0)

    s3 = Soldier(10, 10, 0.5, 3, 0, 'north', 'standing', 10, 0.2, 1)
    s4 = Soldier(10, 10, 0.5, 3, 0, 'north', 'standing', 10, 0.2, 1)

    fb = FactionBuilder()
    fb.build_factions([s1, s2, s3, s4])

    # es necesario definir la posicion de cada soldado en forma de tupla (soldado, posicion)
    soldier_pos = [(s1, (0, 0)), (s2, (0, 2)), (s3, (4, 0)), (s4, (4, 2))]

    """
    weapons
    params:
    name : str
    weight : double
    w_effective_range
    w_max_range
    effective_range_precision
    max_range_precision,
    damage
    damage_area
    fire_rate
    ammunition_capacity
    current_ammo
    reliability
    """

    s1.weapons = [Weapon(*default_weapons['Barret']), Weapon(*default_weapons['Beretta M9'])]
    s1.w_affinities['Barret'] = 1.2
    s1.w_affinities['Beretta M9'] = 1
    s1.weapon_ammo['Beretta M9'] = 20
    s1.weapon_ammo['Barret'] = 50
    s1.equipped_weapon = s1.weapons[0]

    s2.weapons = [Weapon(*default_weapons['M4'])]
    s2.w_affinities['M4'] = 1.2
    s2.weapon_ammo['M4'] = 50
    s2.equipped_weapon = s2.weapons[0]

    s3.weapons = [Weapon(*default_weapons['M4'])]
    s3.w_affinities['M4'] = 1.2
    s3.weapon_ammo['M4'] = 50
    s3.equipped_weapon = s3.weapons[0]

    s4.weapons = [Weapon(*default_weapons['M16']), Weapon(*default_weapons['Beretta M9'])]
    s4.w_affinities['M16'] = 1.2
    s4.w_affinities['Beretta M9'] = 1
    s4.weapon_ammo['Beretta M9'] = 20
    s4.weapon_ammo['M16'] = 50
    s4.equipped_weapon = s4.weapons[0]

    # ab = ActionBuilder(weather, mapa)
    heur = HeuristicManager()
    sim = SimulationManager(fb.get_factions(), weather, sim_map=mapa, heuristics=heur, max_depth=5)
    initial_state = sim.build_initial_state(sim.fractions, sim.ab.am, soldier_pos)

    btf = BattleField(sim, output_dest)
    btf.run_battlefield(soldier_pos)
    return (btf, soldier_pos)