import random
import requests
from settings import TG_TOKEN


def message_handler(text: str, param: dict) -> dict:

    if text == '/help':
        param['ANSWER'] = '''Это тестовый бот для обучения.
        Сейчас он должен научиться играть в игру "Угадай число"
        Для начала игры введите "/game"'''
    elif param['game_started']:
        param = play_game(text, param)
    elif text == '/game':
        param['game_started'] = True
        param['hidden_number'] = random.randint(0, 99)
        param['count'] = 5
        param['ANSWER'] = f"Я загадал число от 0 до 99, попробуй отгадать, у тебя {param['count']} попыток"
    else:
        param['ANSWER'] = text

    return param


def play_game(text: str, param: dict) -> dict:

    if not text.isdigit():
        param['ANSWER'] = 'Введите цело число от 0 до 99'
        return param

    number = float(text)
    if number % 1:
        param['ANSWER'] = 'Загадано целое число'
    elif not 0 <= number < 100:
        param['ANSWER'] = 'Загадано число от 0 до 99'
    else:
        diff = number - param['hidden_number']
        param['count'] -= 1
        if diff == 0:
            param['game_started'] = False
            param['ANSWER'] = f"Ты угадал c {5-param['count']} попытки - загаданное число {param['hidden_number']}"
        elif param['count'] == 0:
            param['game_started'] = False
            param['ANSWER'] = f"У тебя не осталось попыток - загаданное число {param['hidden_number']}"
        elif diff > 0:
            param['ANSWER'] = f"Загаданное число меньше {number}, у тебя осталось {param['count']} попытки"
        elif diff < 0:
            param['ANSWER'] = f"Загаданное число больше {number}, у тебя осталось {param['count']} попытки"
        else:
            param['ANSWER'] = 'такого не должно было случиться'
    return param


API_URL = 'https://api.telegram.org/bot'
OFFSET = -2
TIMEOUT = 60
param = {}
param['ANSWER']: str = ''
param['hidden_number']: int = 0
param['count']:int = 0
param['game_started'] = False

while True:

    updates = requests.get(
        f'{API_URL}{TG_TOKEN}/getUpdates?offset={OFFSET+1}&timeout={TIMEOUT}').json()
    if updates['result']:
        for result in updates['result']:
            OFFSET = result['update_id']
            chat_id = result['message']['from']['id']
            text = result['message']['text']
            param = message_handler(text, param)
            requests.get(f"{API_URL}{TG_TOKEN}/sendMessage?chat_id={chat_id}&text={param['ANSWER']}")
