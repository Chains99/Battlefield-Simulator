from sim.Entities.Soldier import Soldier
from sim.Entities.Map import Map
from sim.Entities.Weather import Weather
from sim.Entities.Weapon import Weapon
from sim.A_star.A_star import euclidean_distance
from math import inf


def test2():
    # Crear mapa y clima
    map1 = Map(7, 7)

    # (self, state, wind_speed, wind_direction, visibility_impairment, temperature, humidity):
    weather = Weather('soleado', 0, 'north', 0.02, 1, 1)

    restriction_matrix = [[1, inf, 2, 1, 1, 2, 1],
                          [1, inf, inf, 3, 1, 1, 1],
                          [1, 4, 2, 1, 3, inf, inf],
                          [1, 3, 3, 4, 2, 1, 1],
                          [1, 3, 2, inf, 2, 1, 1],
                          [1, 2, 1, inf, 1, 1, 1],
                          [1, 2, 2, inf, 2, 1, 1]]

    map1.replace_restrictions(restriction_matrix)

    map1.terrain_matrix[0][1].terrain_object = 1
    map1.terrain_matrix[1][1].terrain_object = 1
    map1.terrain_matrix[1][2].terrain_object = 1
    map1.terrain_matrix[2][5].terrain_object = 1
    map1.terrain_matrix[2][6].terrain_object = 1
    map1.terrain_matrix[4][3].terrain_object = 1
    map1.terrain_matrix[5][3].terrain_object = 1
    map1.terrain_matrix[6][3].terrain_object = 1

    # Crear soldados y equipos
    #team 1
    soldiers_pos_team = {1: (0, 0), 2: (6, 4), 3: (0, 6), 4: (5, 1), 5: (3, 6), 6: (1, 3)}

    sol1 = Soldier(1, 5, 2, 0.8, 5, 1, 1, 1, 1, 0, 1)
    sol2 = Soldier(2, 5, 4, 1, 7, 1, 1, 1, 1, 0, 1)
    sol3 = Soldier(3, 5, 5, 0.9, 4, 1, 1, 1, 1, 0, 1)

    sol_list_team1 = [sol1, sol2, sol3]

    #team 2
    sol4 = Soldier(4, 5, 3, 0.9, 6, 1, 1, 1, 1, 0, 2)
    sol5 = Soldier(5, 5, 5, 0.9, 8, 1, 1, 1, 1, 0, 2)
    sol6 = Soldier(6, 5, 4, 1, 5, 1, 1, 1, 1, 0, 2)

    sol_list_team2 = [sol4, sol5, sol6]
    # asignar turnos
    sol_turns = [sol1, sol5, sol3, sol4, sol2, sol6]

    # Agregar soldados al mapa

    for i in range(len(sol_turns)):
        map1.place_soldier(sol_turns[i], soldiers_pos_team[sol_turns[i].id])

    # Definir armas
    single_weapon = Weapon('gun', 1, 3, 6, 1, 0.7, 1, 0, 1, 10, 1, 1)

    # Agregar armas a los soldados
    for item in sol_turns:
        item.equipped_weapon = single_weapon

    def behavior(focus_point, turns):

        inp = ''
        while inp != 'stop':

            while len(sol_list_team1) != 0 or len(sol_list_team2) != 0:
                # cada soldado en su turno
                for sold in turns:
                    inp = input()
                    enemies = sold.detect_enemies(soldiers_pos_team[sold.id], map1.terrain_matrix)
                    # ataca a 1 soldado enemigo
                    if len(enemies) > 0:
                        enemy = map1.terrain_matrix[enemies[0][0]][enemies[0][1]].standing_soldier
                        # Calculamos el dano
                        damage_dealt = sold.shoot(euclidean_distance(soldiers_pos_team[sold.id], enemies[0]), weather.visibility_impairment, enemy.concealment)
                        # Restamos dano a la salud del enemigo
                        enemy.health -= damage_dealt
                        print('soldier {} dealt {} damage to soldier {}, remaining health {}'.format(sold.id, damage_dealt, enemy.id, enemy.health))
                        if enemy.health < 0:
                            print('sold {} died'.format(enemy.id))
                            # Lo eliminamos de la simulacion

                            turns.remove(enemy)
                            if enemy.team == 1:
                                sol_list_team1.remove(enemy)
                            else:
                                sol_list_team2.remove(enemy)
                            map1.remove_soldier(enemies[0])
                    else:
                        # El soldado se mueve hacia focus_point
                        old_pos = soldiers_pos_team[sold.id]
                        new_pos = sold.move_to(soldiers_pos_team[sold.id], focus_point, map1.restriction_matrix, map1.terrain_matrix)
                        soldiers_pos_team[sold.id] = new_pos
                        map1.move_soldier(old_pos, new_pos, sold)
                        print('soldier {} moved to from {} to {}'.format(sold.id, old_pos, new_pos))

    behavior((3, 3), sol_turns)


test2()
