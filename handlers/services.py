from typing import List
from vkbottle.bot import Message
from bot import bot


@bot.on.message(text='Сервисы')
@bot.on.message(payload={'cmd': 'services'})
async def start_cmd(msg: Message):
    t: List[str] = []
    t.append('На текущий момент бот поддерживает следующие сервисы:\n')
    t.append('Amazon Music'),
    t.append('Amazon Store'),
    t.append('Apple Music'),
    t.append('Audius'),
    t.append('Deezer'),
    t.append('Google Music'),
    t.append('Google Play'),
    t.append('iTunes'),
    t.append('Napster'),
    t.append('Pandora'),
    t.append('SoundCloud'),
    t.append('Spinrilla'),
    t.append('Spotify'),
    t.append('Shazam'),
    t.append('Tidal'),
    t.append('Яндекс.Музыка'),
    t.append('YouTube'),
    t.append('VK (частично)'),
    message = '\n'.join(map(str, t))
    await msg.answer(message)
