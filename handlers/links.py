import re
from urllib.parse import quote
from enum import Enum
from typing import List, Optional

from aiohttp import ClientSession
from urlextract import URLExtract
from vkbottle import PhotoMessageUploader
from vkbottle.bot import Message

from bot import bot
from platforms import platforms


class Platform(str, Enum):
    spotify = 'spotify',
    itunes = 'itunes',
    appleMusic = 'appleMusic',
    youtube = 'youtube',
    youtubeMusic = 'youtubeMusic',
    google = 'google',
    googleStore = 'googleStore',
    pandora = 'pandora',
    deezer = 'deezer',
    tidal = 'tidal',
    amazonStore = 'amazonStore',
    amazonMusic = 'amazonMusic',
    soundcloud = 'soundcloud',
    napster = 'napster',
    yandex = 'yandex',
    spinrilla = 'spinrilla',
    audius = 'audius'


class PlatformShort(str, Enum):
    spotify = 's',
    itunes = 'i',
    appleMusic = 'i',
    youtube = 'y',
    youtubeMusic = 'y',
    google = 'g',
    googleStore = 'g',
    pandora = 'p',
    deezer = 'd',
    tidal = 't',
    amazonStore = 'a',
    amazonMusic = 'a',
    soundcloud = 'sc',
    napster = 'n',
    yandex = 'ya',
    spinrilla = 'sp',
    audius = 'au'


def get_streaming_hell_link(type, platform: Platform, id: str) -> str:
    platform_name = Platform(platform).value
    platform_short = PlatformShort[platform_name].value
    return f'https://streaming-hell.com/{type}/{platform_short}/{id}'


async def download_binary(url: str) -> bytes:
    async with ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()


def is_supported_link(url: str) -> bool:
    strings = [
        'audius',
        'music.apple.com',
        'music.amazon.com',
        'amazon.com',
        'deezer',
        'play.google.com',
        'napster',
        'pandora',
        'soundcloud',
        'spotify',
        'spinrilla',
        'tidal',
        'music.yandex.ru',
        'youtube.com',
        'music.youtube.com'
    ]

    for string in strings:
        match = re.search(string, url)
        if match:
            return True
    return False


@bot.on.message()
async def on_message_handler(msg: Message):
    urls = URLExtract().find_urls(msg.text)
    is_group_chat = msg.peer_id > 2e9

    # If message not contain streaming link
    if not urls:
        if not is_group_chat:
            await msg.answer('В сообщении не найдены ссылки на стриминговые сервисы.')
        return

    for url in urls:

        if is_group_chat and not is_supported_link(url):
            return

        # Send bot `typing...`
        await bot.api.messages.set_activity(user_id=msg.from_id, peer_id=msg.peer_id, group_id=msg.group_id,
                                            type='typing')

        message: List[str] = []

        async with ClientSession() as session:
            print(quote(url))
            async with session.get('http://localhost:8000/api/v1/links', params={"url": quote(url)}) as resp:
                result = await resp.json()
                print(result)

                entity = result['entitiesByUniqueId'][result['entityUniqueId']]

                def url_by_platform(platform: Platform) -> Optional[str]:
                    platform_dict = result['linksByPlatform'].get(platform)
                    if platform_dict is not None:
                        return platform_dict.get('url', None)
                    else:
                        return None

                streaming_hell_url = await bot.api.utils.get_short_link(
                    get_streaming_hell_link(id=entity['id'], type=entity['type'], platform=entity['platforms'][0])
                )

                message.append(f"{entity['artistName']} - {entity['title']}")
                message.append(f"{streaming_hell_url.short_url}\n")

                listen_links: list[str] = []
                buy_links: list[str] = []
                for key, value in platforms.items():
                    print(0)
                    print(url_by_platform(key))
                    print(value['isStore'])
                    if url_by_platform(key) and value['isStore'] is False:
                        print(1)
                        short_link = await bot.api.utils.get_short_link(url_by_platform(key))
                        listen_links.append(f"{value['name']} {short_link.short_url}")
                    elif url_by_platform(key) and value['isStore'] is True:
                        print(2)
                        short_link = await bot.api.utils.get_short_link(url_by_platform(key))
                        buy_links.append(f"{value['name']} {short_link.short_url}")

                if listen_links:
                    message.append('🎧 Слушать')
                    message.extend(listen_links)
                if buy_links:
                    message.append('\n🛍 Купить')
                    message.extend(buy_links)

                message = '\n'.join(map(str, message))
                file = await download_binary(entity['thumbnailUrl'])
                vk_thumbnail = await PhotoMessageUploader(bot.api).upload(file)
                await msg.answer(message=message, attachment=vk_thumbnail, dont_parse_links=True)
