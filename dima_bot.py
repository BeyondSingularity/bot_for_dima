import vk_api
import requests
from random import choice
import schedule
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def norm_text(s):
    a = ' '.join(s.split('-'))
    return a[0].upper() + a[1:]


def get_weather():
    sl = {
        'nw': 'north-west',
        'n': 'north',
        'ne': 'north-east',
        'e': 'east',
        'se': 'south-east',
        's': 'south',
        'sw': 'south-west',
        'w': 'west',
        'с': '---'
    }
    toponym_longitude, toponym_lattitude = "37.492311 55.53181".split()

    api_key = '361ec9eb-40ab-41ef-bfe1-3e8c5755ed1d'
    server = 'https://api.weather.yandex.ru/v1/forecast'
    params = {
        'lat': toponym_lattitude,
        'lon': toponym_longitude,
        'lang': 'ru_RU',
        'extra': 'true'
    }
    headers = {'X-Yandex-API-Key': api_key}
    response = requests.get(server, params=params, headers=headers)
    response = response.json()
    useful = response['fact']

    ans = ''
    ans += f"Current temperature - {useful['temp']}°C, feels like {useful['feels_like']}°C.\n"
    ans += f"{norm_text(useful['condition'])}. Pressure is {useful['pressure_mm']} mm Hg.\n"
    ans += f"Wind speed is {useful['wind_speed']}m/s up to {useful['wind_gust']}m/s. Wind's direction is {sl[useful['wind_dir']]}.\n"
    ans += f"Air's humidity is {useful['humidity']}%\n"

    forecast = response['forecasts'][0]
    if useful['daytime'] == 'd':
        ans += f"Sunset will be at {forecast['sunset']}\n"
    else:
        ans += f"Sunrise will be at {forecast['sunrise']}\n"
    return ans


def disc(a, b, c):
    D = b ** 2 - 4 * a * c
    ans =  str(a) + "X^2" + "+" + str(b) + "X" + "+" + str(c) + "=0\n"
    ans += "D = " + str(D) + '\n'
    if D < 0:
        ans += "NO"
    elif D > 0:
        x1 = (- b + D ** 0.5) / (a * 2)
        x2 = (- b - D ** 0.5) / (a * 2)
        ans += "2 roots: " + str(x1) + " and " + str(x2)
    else:
        x1 = (- b + D ** 0.5) / (a * 2)
        ans += "1 root: " + str(x1)
    return ans


def send(id, msg, keyboard=None):
    if keyboard:
        vk.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message=msg,
            keyboard=keyboard.get_keyboard()
        )
    else:
        vk.messages.send(
            peer_id=id,
            random_id=get_random_id(),
            message=msg
        )

token = "f70b5c9412c788c2a0af2627559f8085ae4903c83bbdbbd3991458363ce4a77269266a1df62e6ba669e56"
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session, mode=10)
vk = vk_session.get_api()

keyboard_start = VkKeyboard(one_time=False)
keyboard_start.add_button(label='Hey!', color=VkKeyboardColor.DEFAULT)

keyboard_choose = VkKeyboard(one_time=False)
keyboard_choose.add_button(label='Solving discriminant equation', color=VkKeyboardColor.POSITIVE)
keyboard_choose.add_button(label='Weather forecast', color=VkKeyboardColor.POSITIVE)
keyboard_choose.add_line()
keyboard_choose.add_button(label='exit', color=VkKeyboardColor.NEGATIVE)


my_id = 293865317
dima_id = 291326308
last_page = 0
discriminant = False
weather = False
schedule.every().day.at("09:00").do(get_weather)

for event in longpoll.listen():
    schedule.run_pending()
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.user_id != my_id:
            vk.messages.send(
                peer_id=event.user_id,
                random_id=get_random_id(),
                message="No",
                attachment='photo-184101489_457239051'
            )
        elif event.text == 'Hey!':
            send(event.user_id, "How is life,Dima?")
            send(event.user_id, "What do you want?", keyboard=keyboard_choose)
        elif event.text == 'Solving discriminant equation':
            send(my_id, "I started to do it, send me 3 numbers splitted via space")
            discriminant = True
        elif discriminant:
            try:
                a, b, c = map(float, event.text.split())
            except:
                send(my_id, "You, stupid cunt, it was said black on white: 3 fucking numbers splitted with a space. Try again, you piece of shit")
                continue
            send(my_id, disc(a, b, c), keyboard_choose)
            discriminant = False
        elif event.text == 'Weather forecast':
            send(my_id, get_weather())
        elif event.text == 'exit':
            send(my_id, "Ok, buy!", keyboard=keyboard_start)
        elif event.text == "Начать":
            send(event.user_id, "Hi there", keyboard=keyboard_start)
        else:
            send(event.user_id, "I don't quite understand you...", keyboard=keyboard_start)