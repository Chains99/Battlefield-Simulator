import PySimpleGUI as sg
from Tests.Sim_Test.quick_tests import run_test

"""  MAIN   """


def execute():
    sg.theme("dark")
    menu_def = [['&File', ['&Load']]]

    main_layout = [
        [sg.Text("Code: ")],
        [sg.Multiline(key="Code", disabled=False, size=(80, 20), font='Courier 8', expand_x=True,
                      expand_y=True,
                      write_only=True, autoscroll=True,
                      auto_refresh=True)],
        [sg.Text("Output: ")],
        [sg.Multiline(key="Result", disabled=True, size=(80, 20), font='Courier 8', expand_x=True,
                      expand_y=True,
                      write_only=True, autoscroll=True,
                      auto_refresh=True)],
        [sg.Push(),
         sg.Button('Reset', key='Reset', button_color='grey'), sg.Button('Run', key='Run', button_color='green')]

    ]

    # App Layout
    layout = [
        [sg.MenubarCustom(menu_def, key='-MENU-', font='Aria 10', background_color="white", bar_text_color="white",
                          text_color="black", bar_background_color="grey", tearoff=False)],
        [main_layout]
    ]

    # Window creation
    runing = False
    sim = None
    window = sg.Window("Project", layout, size=(1024, 720), finalize=True)  # window creation
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == 'Reset':
            runing = False
            window['Result'].update([])

        elif runing and sim != None:
            while(not sim[0].run_battlefield(sim[1])):
                pass


        elif event == 'Run':
            runing = True
            sim = run_test(window['Result'])
            while(not sim[0].run_battlefield(sim[1])):
                pass
    window.close()
