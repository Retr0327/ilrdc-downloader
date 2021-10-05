import re
import pydantic
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Dict
from ilrdc.base import DataCleaner, DataDownloader
from ilrdc.util import modify_sound_url, download_url


class GrammarInfo(pydantic.BaseModel):
    """
    The GrammarInfo object keeps track of an item in inventory, including Id, dialect, chinese translation and sound url.`
    """

    Id: str
    dialect: str
    chinese_translation: str
    sound_url: str

    @pydantic.validator("sound_url")
    @classmethod
    def is_soud_url(cls, value) -> str:
        """The is_soud_url method makes sure there is sould_url value definied."""
        if not value:
            return "沒有音檔"

        return modify_sound_url(value)


@dataclass
class GrammarCleaner(DataCleaner):
    """
    The GrammarCleaner objects first extracts the data from the html, and then cleans it.
    """

    soup: BeautifulSoup

    def __post_init__(self) -> None:
        self.table_tag = self.soup.find(class_="template-1")

    def clean_data(self, specified_tag: BeautifulSoup) -> Dict[str, str]:
        """
        Args:
            specified_tag (BeautifulSoup): the specified html tag

        Returns:
            a dict: {
                'ID': '(4-1)a.',
                'dialect': 'maniq ngahi’ i Silan.',
                'chinese_translation': 'Silan 吃地瓜。',
                'sound_url': 'https://ilrdc.tw/grammar/sound/2/4-1-1.mp3'}
            }
        """
        Id = specified_tag.find(class_="code").text.strip()
        dialect = specified_tag.find(class_="ab").text.strip()
        chinese_translation = specified_tag.find(class_="ch").text.strip()
        sound_url = re.search(
            '(?<=src\="\.).*(mp3|wav|ogg|wma)(?="\>\<td)', str(specified_tag)
        ).group()
        data = GrammarInfo(
            Id=Id,
            dialect=dialect,
            chinese_translation=chinese_translation,
            sound_url=f"{sound_url}",
        )
        return data.dict()

    def extract_data(self) -> map:
        tr_lists = self.table_tag.find_all("tr")
        return map(self.clean_data, tr_lists)
