import PySimpleGUI as sg
from Tests.Sim_Test.quick_tests import run_test
from Language.Lexer.Lexer import lexer

"""  MAIN   """


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
    runing = False
    sim = None
    window = sg.Window("Project", layout, size=(1366, 768), finalize=True)  # window creation
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == '-SAVEDIR-':
            runing = True
            with open(values['-SAVEDIR-'], 'w', encoding='UTF8') as file:
                file.write(values["_Code_"])
                filepath = values['-SAVEDIR-']
                _lexer = lexer()
                code = values["_Code_"]
                tokens = _lexer.get_token_manager('a', code)
                window['Result'].print(tokens)


        elif event == 'Reset':
            runing = False
            window['Result'].update([])

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

        elif event == 'Run':
            # with open(filepath, 'w', encoding='UTF8') as file:
            #     file.write(values["_Code_"])
            # runing = True
            _lexer = lexer()
            code = values["_Code_"]
            tokens = _lexer.get_token_manager('a', values["_Code_"])
            window['Result'].print(tokens)
            # sim = run_test(window['Result'])
            # while(not sim[0].run_battlefield(sim[1])):
            #     pass
    window.close()
