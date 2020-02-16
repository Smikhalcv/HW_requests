import PySimpleGUI as sg
import requests
import json

sg.theme('DarkBlue3')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('The text to translate')],
          [sg.InputText(size=(150, 300))],

          [sg.Text('The path to the text file')],
          [sg.InputText(size=(90, 10)), sg.FileBrowse(), sg.Text('If not specified, it is assumed the source directory')],

          [sg.Text('The language from which to translate. Required field')],
          [sg.InputCombo(('ru', 'en', 'fr', 'de', 'es'), size=(15, 1)), sg.Text('Default Russian')],

          [sg.Text('The language on which to translate. Required field')],
          [sg.InputCombo(('ru', 'en', 'fr', 'de', 'es'), size=(15, 1)), sg.Text('Default English')],
          [sg.Output(size=(150, 20))],
          [sg.Button('Ok'), sg.Button('Record'), sg.Button('Exit')]]

# Create the Window
window = sg.Window('Translater', layout)

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    text = values[0]
    link_read_file = values[1]
    language_r = values[2]
    language_t = values[3]

    if event in (None, 'Exit'):  # if user closes window or clicks cancel
        break


    def translate_text(text, language_t, language_r):  # translate text in value text
        if language_r == '':
            language_r = 'ru'
        if language_t == '':
            language_t = 'en'
        params = {
            'key': API_KEY,
            'text': text,
            'lang': '{}-{}'.format(language_r, language_t),
        }
        response = requests.get(URL, params=params)
        json_ = response.json()
        return ''.join(json_['text'])


    if text != '':
        try:
            print(translate_text(text, language_t, language_r))
        except KeyError:
            print('Input text')
            continue


    def translate_file(path, language_t, language_r):
        if language_r == '':
            language_r = 'ru'
        if language_t == '':
            language_t = 'en'
        with open(r'{}'.format(path), encoding='utf-8') as file:
            f = file.read()
            text = ''
            for line in f:
                if line != '\n':
                    text += line
        params = {
            'key': API_KEY,
            'text': text,
            'lang': '{}-{}'.format(language_r, language_t),
        }
        response = requests.get(URL, params=params)
        json_ = response.json()
        return ''.join(json_['text'])


    if link_read_file != '':
        try:
            print(translate_file(link_read_file, language_t, language_r))
        except KeyError:
            print('Input path')
            continue


    def Record():  # funktion for record text, start if use button Record
        sg.theme('DarkBlue3')  # Add a touch of color
        # All the stuff inside your window.
        layout_2 = [[sg.Text('The text to translate')],
                    [sg.InputText(size=(100, 200))],

                    [sg.Text('The path to readable file')],
                    [sg.InputText(size=(90, 10)), sg.FileBrowse()],

                    [sg.Text('Name the file for record')],
                    [sg.InputText(size=(100, 200)), sg.Text('File extension .json')],

                    [sg.Text('The path to file for record')],
                    [sg.InputText(size=(90, 10)), sg.FolderBrowse()],

                    [sg.Text('The language from which to translate. Required field')],
                    [sg.InputCombo(('ru', 'en', 'fr', 'de', 'es'), size=(10, 1)), sg.Text('Default Russian')],

                    [sg.Text('The language on which to translate. Required field')],
                    [sg.InputCombo(('ru', 'en', 'fr', 'de', 'es'), size=(10, 1)), sg.Text('Default English')],
                    [sg.Output(size=(100, 5))],
                    [sg.Button('Ok'), sg.Button('Cancel')]]

        # Create the Window
        window = sg.Window('Record', layout_2)

        while True:
            event, values = window.read()
            text = values[0]
            path_to_read_file = values[1]
            file_name = values[2]
            path_to_file_record = values[3]
            language_r = values[4]
            language_t = values[5]

            if event in (None, 'Cancel'):  # if user closes window or clicks cancel
                break

            def translate_text_for_record(text, language_t, language_r):  # translate text in value text for record
                if language_r == '':
                    language_r = 'ru'
                if language_t == '':
                    language_t = 'en'
                params = {
                    'key': API_KEY,
                    'text': text,
                    'lang': '{}-{}'.format(language_r, language_t),
                }
                response = requests.get(URL, params=params)
                json_ = response.json()
                return ''.join(json_['text'])

            if text != '':  # if have text, record text in file
                if file_name != '':
                    if path_to_file_record == '':
                        path = file_name
                    if path_to_file_record != '':
                        path = r'{}\{}.json'.format(path_to_file_record, file_name)
                    with open(path, 'w', encoding='utf-8') as file:
                        article = translate_text_for_record(text, language_t, language_r)
                        json.dump(article, file, ensure_ascii=False, indent=2)
                        print('File {} record'.format(file_name))
                else:
                    print('Enter name file')

            def translate_file_for_record(path, language_t, language_r):
                if language_r == '':
                    language_r = 'ru'
                if language_t == '':
                    language_t = 'en'
                with open(r'{}'.format(path), encoding='utf-8') as file:
                    f = file.read()
                    text = ''
                    for line in f:
                        if line != '\n':
                            text += line
                params = {
                    'key': API_KEY,
                    'text': text,
                    'lang': '{}-{}'.format(language_r, language_t),
                }
                response = requests.get(URL, params=params)
                json_ = response.json()
                return ''.join(json_['text'])

            if path_to_read_file != '':  # algoritm record file from def translate_file_for_record
                if file_name != '':
                    if path_to_file_record == '':
                        path = file_name
                    if path_to_file_record != '':
                        path = r'{}\{}.json'.format(path_to_file_record, file_name)
                    with open(path, 'w', encoding='utf-8') as file:
                        article = translate_file_for_record(path_to_read_file, language_t, language_r)
                        json.dump(article, file, ensure_ascii=False, indent=2)
                        print('File {} record'.format(file_name))
                else:
                    print('Enter name file')

        window.close()


    if event == 'Record':
        Record()

window.close()