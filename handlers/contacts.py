from typing import List
from vkbottle.bot import Message
from bot import bot


@bot.on.message(text='Контакты')
@bot.on.message(payload={'command': 'contacts'})
async def contacts(msg: Message):
    t: List[str] = []
    t.append('Сайт проекта https://streaming-hell.com'),
    t.append('Бот в Telegram: https://telegram.me/streaminghell_bot'),
    t.append('Группа VK: https://vk.com/streaminghell')
    message = '\n'.join(map(str, t))
    await msg.answer(message, dont_parse_links=True)
