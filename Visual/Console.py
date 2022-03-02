import PySimpleGUI as sg

from Language.Grammar.grammar import Grammar, non_term_heads, bfs_start
from Language.Lexer.Token import Token, TokenType
from Language.Parser.lr1_parser import LR1Parser
from Language.Lexer.Lexer import lexer
from Language.Parser.ast import Context, FuncDef
from Language.Semantic.Type_checking.type import Type
from Language.Semantic.ast_transpiler import ASTtranspiler


def build_initial_context():
    context = Context('root')
    Type(context, 'Number')
    Type(context, 'Bool')
    Type(context, 'List')
    Type(context, 'String')
    Type(context, 'Void')
    Type(context, 'function')
    soldier = Type(context, 'Soldier')
    weapon = Type(context, 'Weapon')
    terrain = Type(context, 'Terrain')
    weather = Type(context, 'Weather')
    map = Type(context, 'Map')

    # SOLDIER
    soldier.add_attribute('id', 'Number')
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

    soldier.define_function('get_map', 'Map', [], [])
    soldier.define_function('set_weapons', 'Void', ['weapons'], ['List'])
    soldier.define_function('set_affinity', 'Void', ['weapon_name', 'value'], ['String', 'Number'])
    soldier.define_function('set_position', 'Void', ['row', 'col'], ['Number', 'Number'])
    soldier.define_function('set_equiped_weapon', 'Void', ['weapon'], ['String'])
    soldier.define_function('add_extra_action', 'Void', ['action'], ['function'])
    soldier.define_function('remove_extra_action', 'Void', ['index'], ['Number'])

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

    # WEATHER
    weather.add_attribute('state', 'String')
    weather.add_attribute('wind_speed', 'Number')
    weather.add_attribute('visibility_impairment', 'Number')
    weather.add_attribute('temperature', 'Number')
    weather.add_attribute('humidity', 'Number')

    # MAP

    # TERRAIN
    terrain.add_attribute('floor_type', 'String')
    terrain.add_attribute('height', 'Number')
    terrain.add_attribute('m_restriction', 'Number')
    terrain.add_attribute('camouflage', 'Number')
    terrain.add_attribute('available', 'Bool')
    terrain.add_attribute('terrain_object', 'Bool')

    # HEURISTIC

    # BUILDERS
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
    context.add_func(FuncDef('Map', 'Map',
                             ['row', 'col'],
                             ['Number', 'Number'], None))
    context.add_func(FuncDef('Weapon', 'Weapon',
                             ['name', 'weight', 'w_effective_range', 'w_max_range', 'effective_range_precision',
                              'max_range_precision',
                              'damage', 'fire_rate', 'ammunition_capacity', 'current_ammo'],
                             ['String', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number', 'Number',
                              'Number'], None))

    context.add_func(FuncDef('len', 'Number', ['list'], ['List'], None))
    context.add_func(FuncDef('print', 'Void', ['text'], ['String'], None))
    context.add_func(FuncDef('run', 'Void', ['map', 'weather', 'soldiers', 'ia_max_depth'],
                             ['Map', 'Weather', 'List Soldier', 'Number'], None))

    return context


"""  MAIN   """


# def run(runing, window, btf):
#     # si esta corriendo la simulacion ejecutamos un paso
#     if runing[0]:
#         # si el battlefield no ha sido creado, lo creamos
#         if btf[0] is None:
#             btf[0] = run_test(window['Result'])
#         finished = btf[0][0].run_battlefield(btf[1])
#         # comprobamos si termino la simulacion
#         if finished:
#             runing[0] = False


def execute():
    sg.theme("dark")
    menu_def = [['&File', ['&Nothing']]]

    main_layout = [
        [sg.Text("Code: ")],
        [sg.Multiline(key="_Code_", disabled=False, size=(80, 20), font='Courier 8', expand_x=True,
                      expand_y=True,
                      autoscroll=True,
                      auto_refresh=True)],
        [sg.Push(),
         sg.In(size=(25, 1), enable_events=True, key="-LOADDIR-", visible=False),
         sg.FileBrowse('Load', key='load', button_color='grey', file_types=(("SCR", ".scr"),)),
         sg.In(size=(25, 1), enable_events=True, key="-SAVEDIR-", visible=False),
         sg.SaveAs("Save", key="Run_S", file_types=(("SCR", ".scr"),),
                   button_color="blue"),
         sg.Button('Run', key='Run', button_color='green'),
         ],
        [sg.Text("Output: ")],
        [sg.Multiline(key="Result", disabled=True, size=(80, 20), font='Courier 8', expand_x=True,
                      expand_y=True,
                      write_only=True, autoscroll=True,
                      auto_refresh=True)],
        [sg.Push(),
         sg.Button('Reset', key='Reset', button_color='grey')]
    ]

    # App Layout
    layout = [
        [sg.MenubarCustom(menu_def, key='-MENU-', font='Aria 10', background_color="white", bar_text_color="white",
                          text_color="black", bar_background_color="grey", tearoff=False)],
        [main_layout]
    ]

    # Window creation
    filepath = ""
    runing = [False]
    btf = [None]
    window = sg.Window("Project", layout, size=(1366, 768), finalize=True)  # window creation

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED:
            break

        elif event == '-SAVEDIR-':
            with open(values['-SAVEDIR-'], 'w', encoding='UTF8') as file:
                file.write(values["_Code_"])
                filepath = values['-SAVEDIR-']


        elif event == 'Reset':
            runing = [False]
            btf = [None]
            window['Result'].update("")

        # elif runing and sim != None:
        #     while(not sim[0].run_battlefield(sim[1])):
        #         pass

        elif event == "-LOADDIR-":
            try:
                with open(values["-LOADDIR-"]) as file:
                    script = file.read()
                    window['_Code_'].update(script)
                    filepath = values["-LOADDIR-"]
            except:
                sg.Popup('error')

        elif event == '__TIMEOUT__':
            if runing[0]:
                pass
                # run(runing, window, btf)

        elif event == 'Run':
            # mandamos a correr el proyecto(test por ahora)
            # if not runing[0]:
            #     runing[0] = True
            #     run(runing, window, btf)

            # tokenizing
            lex = lexer()
            tokens = lex.get_token_manager("file", values['_Code_']).tokens
            tokens.append(Token("EOF", "EOF", TokenType.EOF))

            # parsing
            grammar = Grammar(non_term_heads, bfs_start)
            parser = LR1Parser(grammar)
            ast = parser.parse(tokens)
            python_code = ASTtranspiler().transpile(ast, build_initial_context())
            window['Result'].print(python_code)
    window.close()
