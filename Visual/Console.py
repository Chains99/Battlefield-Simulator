import PySimpleGUI as sg
from Tests.Sim_Test.quick_tests import run_test
from Language.Lexer.Lexer import lexer

"""  MAIN   """


def run(runing, window, btf):
    # si esta corriendo la simulcion ejecutamos un paso
    if runing[0]:
        # si el battlefield no ha sido creado, lo creamos
        if btf[0] is None:
            btf[0] = run_test(window['Result'])
        finished = btf[0][0].run_battlefield(btf[1])
        # comprobamos si termino la simulacion
        if finished:
            runing[0] = False


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
                run(runing, window, btf)

        elif event == 'Run':
            # mandamos a correr el proyecto(test por ahora)
            # if not runing[0]:
            #     runing[0] = True
            #     run(runing, window, btf)
            lex = lexer()
            tokens = lex.get_token_manager("file", values['_Code_'])
            window['Result'].print(tokens)
    window.close()
