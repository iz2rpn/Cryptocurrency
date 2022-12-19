import PySimpleGUI as sg
from crypto import Crypto


def main():
    sg.theme('DarkBlue')

    layout = [
        [sg.Text('Search for a crypto. E.g BTC or MATIC')],
        [sg.Image(size=(64, 64), key='-LOGO-'), sg.Input(key='-INPUT-')],
        [sg.Text(key='-NAME-', justification='center', font=("Helvetica", 16), border_width=1)],
        [sg.Text('Price: '), sg.Text(key='-VALUTA-')],
        [sg.Text('Volume: '), sg.Text(key='-VOLUME-')],
        [sg.Button('Update', key='-UPDATE-'), sg.Button("Close")]]

    window = sg.Window('Cryptocurrency', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Close":
            break

        if event == "-UPDATE-":
            current_crypto = Crypto(values["-INPUT-"])
            window["-VALUTA-"].update(f"{current_crypto.value:,.0f} €")
            window["-VOLUME-"].update(f"{current_crypto.volume:,.0f} €")
            window["-NAME-"].update(current_crypto.name)
            window["-LOGO-"].update(current_crypto.logoImg)



if __name__ == '__main__':
    main()
