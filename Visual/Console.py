import PySimpleGUI as sg

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
        [sg.Push(), sg.Button('Stop', key='Reset', button_color='red'),
         sg.Button('Reset', key='Reset', button_color='grey'), sg.Button('Run', key='Run', button_color='green')]

    ]

    # App Layout
    layout = [
        [sg.MenubarCustom(menu_def, key='-MENU-', font='Aria 10', background_color="white", bar_text_color="white",
                          text_color="black", bar_background_color="grey", tearoff=False)],
        [main_layout]
    ]

    # Window creation
    stoped = False
    window = sg.Window("Project", layout, size=(1024, 720), finalize=True)  # window creation
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event != 'Stop' != 'Run' and stoped:
            continue

        elif event == 'Reset':
            stoped = False
            window['Result'].update([])

        elif event == 'Stop':
            stoped = True
            continue

        elif event == 'Run':
            stoped = False
            break

    window.close()
