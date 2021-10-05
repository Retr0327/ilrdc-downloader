import aiohttp
from bs4 import BeautifulSoup


async def download_url(url) -> BeautifulSoup:
    """The download_url function downloads the url.

    Args:
        url (str): the url

    Returns:
        a BeautifulSoup object
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")
            return soup


def modify_sound_url(sound_url) -> str:
    """The modify_sound_url function modifies the sound url because sometimes the sound url in the website
       does not have the correct form, such as `.sound/6/4-1-3mp3` instead of `.sound/6/4-1-3.mp3`.

    Args:
        sound_url (str): the sound url

    Returns:
        a str
    """

    sound_type = sound_url[-4:]
    if "." not in sound_type:
        modified_url = sound_url.replace(sound_url[-3:], f".{sound_url[-3:]}")
        return f"https://ilrdc.tw/grammar{modified_url}"

    return f"https://ilrdc.tw/grammar{sound_url}"
