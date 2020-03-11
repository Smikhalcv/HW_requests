import requests
import json
from pprint import pprint

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def text():
    data = input('Укажите текст или файл, который хотите перевести: ')
    if data.endswith('.txt'):
        try:
            with open(r'{}'.format(data), encoding='utf-8') as file:
                f = file.read()
                text = ''
                for line in f:
                    if line != '\n':
                        text += line
        except FileNotFoundError:
            print('Файл указан неверно или не существует')
    else:
        text = data

    language_t = input('''Укажите язык с которого нужно перевести.
Если язык не указан или указан не правильно будет выбран Английский!
Доступные языки:
    'en' - английсикй, 'ru' - руссикий, 'de' - немецкий,  'fr' - французский, 'es' - испанский
    ''').lower()

    if language_t not in ['ru', 'de', 'fr', 'es', 'en']:
        language_t = 'en'

    language_r = input('''Укажите язык на который нужно перевести.
Если язык не указан или указан не правильно будет выбран Русский!
Доступные языки:
    'en' - английсикй, 'ru' - руссикий, 'de' - немецкий,  'fr' - французский, 'es' - испанский
    ''').lower()

    if language_r not in ['ru', 'de', 'fr', 'es', 'en']:
        language_r = 'ru'

    return text, language_t, language_r


def operation():
    while True:
        action = input('''Укажите действие с текстом.
'trans' - перевод, 'rec' - запись в файл
''').lower()
        if action == 'trans' or action == 'rec':
            break
    return action


def translater_record():
    data, language_read, language_trans = text()
    action = operation()
    params = {
        'key': API_KEY,
        'text': data,
        'lang': '{}-{}'.format(language_read, language_trans),
    }
    response = requests.get(URL, params=params)
    json_response = response.json()
    translated_text = json_response['text']

    if action == 'trans':
        pprint(translated_text)
    if action == 'rec':
        while True:
            file_name = input('''Укажите имя файла.
Файлу будет формата json.
''')
            if file_name != '':
                path_to_file_record = input('''Укажите путь в файлу. 
Если путь не указал, то файл будет создан в директории программы.
                ''')
                if path_to_file_record == '':
                    path = file_name
                if path_to_file_record != '':
                    path = r'{}\{}.json'.format(path_to_file_record, file_name)
                break
        with open(path, 'w', encoding='utf-8') as file:
            article = translated_text
            json.dump(article, file, ensure_ascii=False, indent=2)
            print('File {} record'.format(file_name))


def main():
    while True:
        translater_record()
        response = input('''Хотите продолжить работу с программой? (да/нет)
        ''').lower()
        if response.startswith('н'):
            break


if __name__ in '__main__':
    main()
