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
from IA.Action_manager import ActionManager
from Sim.aux_actions import aux_action

"""
def run_test(output_dest):
    
    mapa = Map(5, 5)
    weather = Weather(0, 0, 1.2, 0, 0)
    mapa.terrain_matrix[0][2].add_object(True)
   
    s1 = Soldier(100, 10, 0.5, 6, 0, 'north', 'standing', 10, 0.2, 10, 0)
    s2 = Soldier(100, 10, 0.5, 2, 0, 'north', 'standing', 10, 0.2, 10, 0)

    s3 = Soldier(100, 10, 0.5, 3, 0, 'north', 'standing', 10, 0.2, 11, 1)
    s4 = Soldier(100, 10, 0.5, 3, 0, 'north', 'standing', 10, 0.2, 12, 1)

    fb = FactionBuilder()
    fb.build_factions([s1, s2, s3, s4])
    #fb.build_factions([s1, s3])

    # es necesario definir la posicion de cada soldado en forma de tupla (soldado, posicion)
    soldier_pos = [(s1, (0, 0)), (s2, (0, 2)), (s3, (4, 0)), (s4, (4, 2))]
    s1.position = (0, 0)
    s2.position = (0, 2)
    s3.position = (4, 0)
    s4.position = (4, 2)
    #soldier_pos = [(s1, (0, 0)), (s3, (4, 0))]

    
    

    s1.weapons = [Weapon(*default_weapons['Barret']), Weapon(*default_weapons['Beretta M9'])]
    s1.w_affinities['Barret'] = 1.2
    s1.w_affinities['Beretta M9'] = 1
    s1.weapon_ammo['Beretta M9'] = 0
    s1.weapon_ammo['Barret'] = 0
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
    fb.factions[0].heuristic = heur
    fb.factions[1].heuristic = heur
    sim = SimulationManager(fb.get_factions(), weather, sim_map=mapa, max_depth=2)
    initial_state = sim.build_initial_state(sim.fractions, sim.ab.am)


    # DECO TEST
    fun = ActionManager.detect_enemies
    fun2 = aux_action(initial_state)(fun)
    #fun2 = fun2(fun)

    res = fun2(sim.ab.am, s1)


    btf = BattleField(sim, output_dest)
    btf.run_battlefield()
    return btf, soldier_pos


run_test(None)
"""
