from typing import List
from vkbottle.bot import Message
from vkbottle import Keyboard, Text
from bot import bot


@bot.on.message(text='Начать')
@bot.on.message(payload={'cmd': 'start'})
async def start_cmd(msg: Message):
    t: List[str] = []
    t.append('👋 Привет!')
    t.append('Моя основная функция – искать музыку во всех (почти) стриминогвых сервисах.')
    t.append('Отправь мне ссылку или несколько ссылок на трек или альбом из любого стримингового .сервиса, а в ответ я пришлю ссылки на другие сервисы, где я нашёл твой трек или альбом.')
    t.append('Список поддерживаемых на данный момент сервисов можно получить командой Сервисы')
    message = '\n\n'.join(map(str, t))
    keyboard = Keyboard(one_time=False, inline=False).add(Text("Начать", payload={'command': 'start'})).add(Text("Контакты", payload={'command': 'contacts'})).add(Text("Сервисы", payload={'command': 'services'}))
    await msg.answer(message=message, keyboard=keyboard)
