import PySimpleGUI as sg
from Language.Grammar.grammar import Grammar, non_term_heads, bfs_start
from Language.Lexer.Token import Token, TokenType
from Language.Parser.lr1_parser import LR1Parser
from Language.Lexer.Lexer import lexer
from Language.Parser.ast import Context
from Language.Semantic.ast_transpiler import ASTtranspiler
from Sim.Entities.Soldier import Soldier
from Sim.battlefield import build_battlefield, BattleField

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


def run(map, weather, soldiers: Soldier, ia_max_depth: int):
    btf = build_battlefield(map, weather, soldiers, ia_max_depth)
    Manager.runing = True
    Manager.btf = btf
    run_btf(btf)


def execute(context:Context):
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
                      auto_refresh=True, reroute_stdout=True)],
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
            if Manager.runing and Manager.f_execution and not Manager.end:
                run_btf(Manager.btf)

        elif event == 'Run':
            # mandamos a correr el proyecto(test por ahora)
            # if not runing[0]:
            #     runing[0] = True
            #     run(runing, window, btf)
            if (not Manager.runing):
                # tokenizing
                lex = lexer()
                tokens = lex.get_token_manager("file", values['_Code_']).tokens
                tokens.append(Token("EOF", "EOF", TokenType.EOF))

                # parsing
                grammar = Grammar(non_term_heads, bfs_start)
                parser = LR1Parser(grammar)
                ast = parser.parse(tokens)
                translated_code = ASTtranspiler().transpile(ast, context)
                #window['Result'].print(translated_code)
                exec(translated_code, globals())
    window.close()
