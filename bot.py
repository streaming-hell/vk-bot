from os import getenv
from vkbottle.bot import Bot

API_KEY = getenv('API_KEY')
if not API_KEY:
    exit("Error: no API_KEY provided")

bot = Bot(token=API_KEY)
