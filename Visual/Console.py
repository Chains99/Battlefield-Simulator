import functools
import sys
import types
from collections import deque

import PySimpleGUI as sg
from Language.Grammar.grammar import Grammar, non_term_heads, bfs_start
from Language.Parser.lr1_parser import LR1Parser
from Language.Lexer.Lexer import lexer
from Language.Parser.ast import Context, FuncDef
from Language.Semantic.Type_checking.Type import Type
from Language.Semantic.ast_transpiler import ASTtranspiler, AuxActions
from Sim.Entities.Soldier import Soldier
from Sim.battlefield import build_battlefield, BattleField


def build_initial_context():
    context = Context('root')
    Type(context, 'Number')
    Type(context, 'Bool')
    Type(context, 'String')
    Type(context, 'Void')
    Type(context, 'function')
    soldier = Type(context, 'Soldier')
    weapon = Type(context, 'Weapon')
    terrain = Type(context, 'Terrain')
    weather = Type(context, 'Weather')
    Type(context, 'List')
    list_S = Type(context, 'List Soldier')
    list_S.define_function('append', 'Void', ['soldier'], ['Soldier'])
    list_N = Type(context, 'List Number')
    list_N.define_function('append', 'Void', ['Number'], ['Number'])
    list_B = Type(context, 'List Bool')
    list_B.define_function('append', 'Void', ['Bool'], ['Bool'])
    list_Str = Type(context, 'List String')
    list_Str.define_function('append', 'Void', ['String'], ['String'])
    list_V = Type(context, 'List Void')
    list_V.define_function('append', 'Void', ['Void'], ['Void'])
    list_W = Type(context, 'List Weapon')
    list_W.define_function('append', 'Void', ['Weapon'], ['Weapon'])
    list_T = Type(context, 'List Terrain')
    list_T.define_function('append', 'Void', ['Terrain'], ['Terrain'])
    list_We = Type(context, 'List Weather')
    list_We.define_function('append', 'Void', ['Weather'], ['Weather'])
    list_H = Type(context, 'HeuristicManager')
    list_H.define_function('append', 'Void', ['HeuristicManager'], ['HeuristicManager'])
    aux_actions = Type(context, 'AuxActions')
    map = Type(context, 'Map')

    # SOLDIER
    soldier.add_attribute('health', 'Number')
    soldier.add_attribute('current_health', 'Number')
    soldier.add_attribute('vision_range', 'Number')
    soldier.add_attribute('precision', 'Number')
    soldier.add_attribute('move_speed', 'Number')
    soldier.add_attribute('crit_chance', 'Number')
    soldier.add_attribute('orientation', 'String')
    soldier.add_attribute('stance', 'String')
    soldier.add_attribute('max_load', 'Number')
    soldier.add_attribute('concealment', 'Number')
    soldier.add_attribute('melee_damage', 'Number')
    soldier.add_attribute('equipped_weapon', 'Weapon')

    soldier.define_function('get_map', 'Map', [], [])
    soldier.define_function('set_weapons', 'Void', ['weapons', 'magazines'], ['List Weapon', 'List Number'])
    soldier.define_function('set_affinity', 'Void', ['weapon_name', 'value'], ['String', 'Number'])
    soldier.define_function('set_current_health', 'Void', ['health'], ['Number'])
    soldier.define_function('set_vision_range', 'Void', ['health'], ['Number'])
    soldier.define_function('set_precision', 'Void', ['precision'], ['Number'])
    soldier.define_function('set_move_speed', 'Void', ['move_speed'], ['Number'])
    soldier.define_function('set_crit_chance', 'Void', ['crit_chance'], ['Number'])
    soldier.define_function('set_max_load', 'Void', ['max_load'], ['Number'])
    soldier.define_function('set_concealment', 'Void', ['concealment'], ['Number'])
    soldier.define_function('set_melee_damage', 'Void', ['concealment'], ['Number'])
    soldier.define_function('set_position', 'Void', ['map', 'row', 'col'], ['Map', 'Number', 'Number'])
    soldier.define_function('set_equiped_weapon', 'Void', ['weapon'], ['String'])
    soldier.define_function('add_extra_action', 'Void', ['action'], ['function'])
    soldier.define_function('remove_extra_action', 'Void', ['index'], ['Number'])
    soldier.define_function('get_team', 'Number', [], [])
    soldier.define_function('is_ally', 'Bool', ['soldier'], ['Soldier'])

    # WEAPON
    weapon.add_attribute('name', 'String')
    weapon.add_attribute('weight', 'Number')
    weapon.add_attribute('w_effective_range', 'Number')
    weapon.add_attribute('w_max_range', 'Number')
    weapon.add_attribute('effective_range_precision', 'Number')
    weapon.add_attribute('max_range_precision', 'Number')
    weapon.add_attribute('damage', 'Number')
    weapon.add_attribute('fire_rate', 'Number')
    weapon.add_attribute('ammunition_capacity', 'Number')
    weapon.add_attribute('current_ammo', 'Number')

    weapon.define_function('set_name', 'Void', ['a'], ['String'])
    weapon.define_function('set_weight', 'Void', ['a'], ['Number'])
    weapon.define_function('set_w_effective_range', 'Void', ['a'], ['Number'])
    weapon.define_function('set_w_max_range', 'Void', ['a'], ['Number'])
    weapon.define_function('set_effective_range_precision', 'Void', ['a'], ['Number'])
    weapon.define_function('set_damage', 'Void', ['a'], ['Number'])
    weapon.define_function('set_fire_rate', 'Void', ['a'], ['Number'])
    weapon.define_function('set_current_ammo', 'Void', ['a'], ['Number'])

    # WEATHER
    weather.add_attribute('state', 'String')
    weather.add_attribute('wind_speed', 'Number')
    weather.add_attribute('visibility_impairment', 'Number')
    weather.add_attribute('temperature', 'Number')
    weather.add_attribute('humidity', 'Number')

    # MAP
    map.add_attribute('rows', 'Number')
    map.add_attribute('cols', 'Number')
    map.define_function('set_object', 'Void', ['row', 'col'], ['Number', 'Number'])
    map.define_function('remove_object', 'Void', ['row', 'col'], ['Number', 'Number'])
    map.define_function('get', 'Terrain', ['row', 'col'], ['Number', 'Number'])

    # TERRAIN
    terrain.add_attribute('floor_type', 'String')
    terrain.add_attribute('height', 'Number')
    terrain.add_attribute('m_restriction', 'Number')
    terrain.add_attribute('camouflage', 'Number')
    terrain.add_attribute('available', 'Bool')
    terrain.add_attribute('terrain_object', 'Bool')

    terrain.define_function('set_m_restriction', 'Void', ['m_restriction'], ['Number'])
    terrain.define_function('set_camouflage', 'Void', ['camouflage'], ['Number'])

    # HEURISTIC

    # AUX_ACTIONS
    aux_actions.define_function(
        'detect_enemies_within_eff_range', 'List Soldier', ['soldier', 'map'], ['Soldier', 'Map'])

    aux_actions.define_function(
        'detect_enemies_within_max_range', 'List Soldier', ['soldier', 'map'], ['Soldier', 'Map'])

    aux_actions.define_function(
        'detect_allies', 'List Soldier', ['soldier', 'map'], ['Soldier', 'Map'])

    aux_actions.define_function(
        'shoot', 'Void', ['soldierA', 'soldierB'], ['Soldier', 'Soldier'])

    aux_actions.define_function(
        'get_position', 'List Number', ['soldierA', 'soldierB'], ['Soldier', 'Soldier'])

    aux_actions.define_function(
        'move', 'Void', ['soldier', 'position'], ['Soldier', 'List Number'])

    # TYPE INSTANCE BUILDERS
    context.add_func(FuncDef('Soldier', 'Soldier',
                             ['health', 'vision_range', 'precision', 'move_speed', 'crit_chance', 'orientation',
                              'stance', 'max_load', 'concealment', 'melee_damage', 'team'],
                             ['Number', 'Number', 'Number', 'Number', 'Number', 'String', 'String', 'Number', 'Number',
                              'Number', 'Number'], None))
    context.add_func(FuncDef('Terrain', 'Terrain',
                             ['floor_type', 'height', 'm_restriction', 'camouflage', 'available', 'terrain_object'],
                             ['String', 'Number', 'Number', 'Number', 'Bool', 'Bool'], None))
    context.add_func(FuncDef('Weather', 'Weather',
                             ['state', 'wind_speed', 'visibility_impairment', 'temperature', 'humidity'],
                             ['String', 'Number', 'Number', 'Number', 'Number'], None))
    context.add_func(FuncDef('AuxActions', 'AuxActions',
                             [],
                             [], None))
    context.add_func(FuncDef('Map', 'Map',
                             ['row', 'col'],
                             ['Number', 'Number'], None))
    context.add_func(FuncDef('Weapon', 'Weapon',
                             ['name', 'weight', 'w_effective_range', 'w_max_range', 'effective_range_precision',
                              'max_range_precision',
                              'damage', 'fire_rate', 'ammunition_capacity', 'current_ammo'],
                             ['String', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number',
                              'Number'], None))
    context.add_func(FuncDef('HeuristicManager', 'HeuristicManager',
                             ['damage_hvalue', 'allies_hvalue', 'enemies_in_sight_hvalue', 'enemies_in_range_hvalue',
                              'low_ammo_hvalue',
                              'concealment_hvalue',
                              'remaining_hvalue', 'dead_hvalue', 'damage_dealt_hvalue'],
                             ['Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number',
                              'Number'], None))

    # AUXILIARY FUNCTIONS
    context.add_func(FuncDef('len', 'Number', ['list'], ['List'], None))
    context.add_func(FuncDef('str', 'String', ['number'], ['Number'], None))
    context.add_func(FuncDef('int', 'Number', ['number'], ['Number'], None))
    context.add_func(FuncDef('print', 'Void', ['text'], ['String'], None))
    context.add_func(FuncDef('run', 'Void', ['map', 'weather', 'soldiers', 'ia_max_depth', 'heuristic'],
                             ['Map', 'Weather', 'List Soldier', 'Number', 'List HeuristicManager'], None))

    return context


# copy func function takes a function and returns a copy of it
def copy_func(func):
    g = types.FunctionType(func.__code__, func.__globals__, name=func.__name__,
                           argdefs=func.__defaults__, closure=func.__closure__)
    g = functools.update_wrapper(g, func)
    g.__kwdefaults__ = func.__kwdefaults__
    return g


"""  MAIN   """


class Manager():
    runing = False
    f_execution = True
    end = False
    btf = None


def run_btf(btf: BattleField):
    # si esta corriendo la simulacion ejecutamos un paso
    Manager.f_execution = False
    if Manager.runing:
        # si el battlefield no ha sido creado, lo creamos
        finished = btf.run_battlefield()
        # comprobamos si termino la simulacion
        Manager.end = finished
        Manager.f_execution = True
        if (Manager.end):
            print("Simulation end")


def reset(original_functions, window):
    Manager.runing = False
    Manager.end = False
    Manager.f_execution = True
    Manager.btf = None
    Soldier.id = 0
    AuxActions.move = copy_func(original_functions[0])
    AuxActions.detect_allies = copy_func(original_functions[1])
    AuxActions.shoot = copy_func(original_functions[2])
    AuxActions.detect_enemies = copy_func(original_functions[3])
    AuxActions.detect_enemies_within_eff_range = copy_func(original_functions[4])
    AuxActions.detect_enemies_within_max_range = copy_func(original_functions[5])
    AuxActions.get_position = copy_func(original_functions[6])
    window['Result'].update("")


sys.setrecursionlimit(100000)


def run(map, weather, soldiers: Soldier, ia_max_depth: int, heuristic):
    if (Manager.runing):
        raise Exception('Solo se puede ejecutar una simulaci\'on por script')
    btf = build_battlefield(map, weather, soldiers, ia_max_depth, heuristic)
    Manager.runing = True
    Manager.btf = btf
    run_btf(btf)


def execute():
    original_functions = [0] * 7
    original_functions[0] = copy_func(AuxActions.move)
    original_functions[1] = copy_func(AuxActions.detect_allies)
    original_functions[2] = copy_func(AuxActions.shoot)
    original_functions[3] = copy_func(AuxActions.detect_enemies)
    original_functions[4] = copy_func(AuxActions.detect_enemies_within_eff_range)
    original_functions[5] = copy_func(AuxActions.detect_enemies_within_max_range)
    original_functions[6] = copy_func(AuxActions.get_position)

    sg.theme("Dark Grey 11")

    main_layout = [
        [sg.Text("Code: ")],
        [sg.Multiline(key="_Code_", disabled=False, size=(40, 20), font='Courier 10', expand_x=True,
                      expand_y=True,
                      autoscroll=True,
                      auto_refresh=True,
                      text_color="yellow", enable_events=True)],
        [sg.Push(),
         sg.In(size=(25, 1), enable_events=True, key="-LOADDIR-", visible=False),
         sg.FileBrowse('Load', key='load', button_color='grey', file_types=(("SCR", ".scr"),)),
         sg.In(size=(25, 1), enable_events=True, key="-SAVEDIR-", visible=False),
         sg.SaveAs("Save", key="Run_S", file_types=(("SCR", ".scr"),),
                   button_color="blue"),
         sg.Button('Run', key='Run', button_color='green'),
         sg.Button('Python Code', key='Python', button_color='blue')
         ],
        [sg.Text("Output: ")],
        [sg.Multiline(key="Result", disabled=True, size=(40, 20), font='Courier 10', expand_x=True,
                      expand_y=True,
                      write_only=True, autoscroll=True,
                      auto_refresh=True, reroute_stdout=True, text_color="light green")],
        [sg.Push(),
         sg.Button('Reset', size=(5, 5), key='Reset', button_color='grey')]
    ]

    # App Layout
    layout = [
        [main_layout]
    ]

    # Window creation
    code = ''
    ctrl_z_stack = deque()
    filepath = ""
    window = sg.Window("Project", layout, size=(1366, 788), finalize=True)  # window creation

    window["_Code_"].bind("<Control-s>", "_Control-s")
    window["_Code_"].bind("<Control-z>", "_Control-z")
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break


        elif event == "_Code_" + '_Control-s':
            if filepath != '':
                with open(filepath, 'w', encoding='UTF8') as file:
                    file.write(values["_Code_"])
            else:
                window['Run_S'].click()

        elif event == "_Code_" + '_Control-z' and len(ctrl_z_stack):
            _new = ctrl_z_stack.pop()
            window['_Code_'].update(_new[0])
            filepath = _new[1]
            code = _new[0]

        elif event == "_Code_":
            if code != values['_Code_']:
                if (len(ctrl_z_stack) == 100):
                    ctrl_z_stack.popleft()
                ctrl_z_stack.append((code, filepath))
                code = values['_Code_']


        elif event == '-SAVEDIR-':
            if not values['-SAVEDIR-'] == '':
                with open(values['-SAVEDIR-'], 'w', encoding='UTF8') as file:
                    file.write(values["_Code_"])
                    filepath = values['-SAVEDIR-']


        elif event == 'Reset':
            reset(original_functions, window)


        elif event == "-LOADDIR-":
            try:
                with open(values["-LOADDIR-"]) as file:
                    script = file.read()
                    window['_Code_'].update(script)
                    filepath = values["-LOADDIR-"]
            except:
                pass

        elif event == '__TIMEOUT__':
            if Manager.runing and Manager.f_execution and not Manager.end:
                run_btf(Manager.btf)

        elif event == 'Python':
            if (not Manager.runing):
                if values['_Code_'] == '':
                    sg.popup('', 'Please write some code as input to run')
                    continue
                window['Result'].update('')
                context = build_initial_context()
                lex = lexer()
                tokens = lex.get_token_manager("file", values['_Code_']).tokens
                # Parsing
                grammar = Grammar(non_term_heads, bfs_start)
                parser = LR1Parser(grammar)
                ast = parser.parse(tokens)
                translated_code = ASTtranspiler().transpile(ast, context)
                window['Result'].print(translated_code)


        elif event == 'Run':
            if (not Manager.runing):
                # try:
                # Tokenizing
                if values['_Code_'] == '':
                    sg.popup('', 'Please write some code as input to run')
                    continue
                window['Result'].update('')
                context = build_initial_context()
                lex = lexer()
                tokens = lex.get_token_manager("file", values['_Code_']).tokens
                # Parsing
                grammar = Grammar(non_term_heads, bfs_start)
                parser = LR1Parser(grammar)
                ast = parser.parse(tokens)
                translated_code = ASTtranspiler().transpile(ast, context)
                window['Result'].update('')
                exec(translated_code, globals())
            # except Exception as e:
            #     window['Result'].print(e, text_color="red")
    window.close()
