
############################################################################
#                                                                          #
# Author: Pietro Marchetta [IZ2RPN]                                        #
#                                                                          #
# Description: This project shows the current currency of a cryptocurrency #
#                                                                          #
############################################################################

from PIL import Image, ImageTk
from urllib import request
import requests
import json
import os
import PySimpleGUI as sg

local_path = os.getcwd()

def get_data(crypt: str):
    headers = {
        'User-Agent': (
                        'Mozilla/5.0 (X11; Linux x86_64)'
                        'AppleWebKit/537.36 (KHTML, like Gecko)' 
                        'Chrome/108.0.0.0 Safari/537.36')}    

    url = f'https://query1.finance.yahoo.com/v7/finance/quote?&symbols={crypt}-EUR'

    icon_error = os.path.join(local_path, "img/nf.png")
    
    try:
        res = requests.get(url, headers=headers)
        value = res.json()["quoteResponse"]["result"][0]["regularMarketPrice"]
        volume = res.json()["quoteResponse"]["result"][0]["regularMarketVolume"]
        logo = res.json()["quoteResponse"]["result"][0]["logoUrl"]
        name = res.json()["quoteResponse"]["result"][0]["shortName"]
        error = 0
    except requests.ConnectionError:
        value = 0
        volume = 0
        logo = icon_error
        error = 1
        name = 'NOT FOUND'
    except IndexError:
        value = 0
        volume = 0
        logo =  icon_error
        error = 1
        name = 'NOT FOUND'
    except KeyError:
        value = 0
        volume = 0
        logo = icon_error
        error = 1
        name = 'NOT FOUND'

    return value, volume, logo, error, name

def logo_update(link):
    # Get one PNG file from website and save to file
    url = (link)
    headers = {
        'User-Agent': (
                        'Mozilla/5.0 (X11; Linux x86_64)'
                        'AppleWebKit/537.36 (KHTML, like Gecko)' 
                        'Chrome/108.0.0.0 Safari/537.36')}

    req = request.Request(url, headers=headers)
    response = request.urlopen(req)


    if response.status != 200:
        print("Failed to load image from website !")
        exit()

    data = response.read()

    filename = os.path.join(local_path, "img/logo.png")
    with open(filename, "wb") as f:
        f.write(data)
    size = (64, 64)
    im = Image.open(filename)
    im = im.resize(size, resample=Image.Resampling.BICUBIC)

    # Convert image
    rgba = im.convert('RGBA')
    image = ImageTk.PhotoImage(image=rgba)

    # update image in sg.Image
    window['-LOGO-'].update(data=image)

sg.theme('DarkBlue')

layout = [
    [sg.Text('Please enter name of cryptovalute. For esample "BTC" or "MATIC"')],
    [sg.Image(size=(64, 64), key = '-LOGO-'),sg.Input(key = '-INPUT-')],
    [sg.Text(key = '-NAME-', justification='center', font=("Helvetica", 16), border_width=1)],
    [sg.Text('Price: '), sg.Text(key = '-VALUTA-')],
    [sg.Text('Volume: '), sg.Text(key = '-VOLUME-')],
    [sg.Button('Aggiorna', key = '-UPDATE-')]]

window = sg.Window('Cryptocurrency',  layout)

while True:
    event, values = window.read()
   
    if event == sg.WIN_CLOSED:
        break
    
    if event == '-UPDATE-':
        input_value = values['-INPUT-']
        window['-VALUTA-'].update(f"{get_data(input_value)[0]:,.2f} €")
        window['-VOLUME-'].update(f"{get_data(input_value)[1]:,.0f} €")
        url_logo = get_data(input_value)[2]
        error = get_data(input_value)[3]
        name = get_data(input_value)[4]

        if error == 0:
            logo_update(url_logo)
            window['-NAME-'].update(name[:-3])
        else:
            window['-LOGO-'].update(url_logo)
            window['-NAME-'].update(name)

window.close()
    
    
