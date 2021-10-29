import re
import pydantic
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Generator, Union, Any
from ilrdc.urldialector import URLDialector
from ilrdc.base import DataCleaner, DataDownloader
from ilrdc.util import modify_sound_url, download_url


class StoryInfo(pydantic.BaseModel):
    dialect: Any
    chinese_translation: Any
    sound_url: Any

    @pydantic.validator("sound_url")
    @classmethod
    def is_soud_url(cls, value: str) -> str:
        """The is_soud_url method makes sure there is sould_url value definied."""
        if value is None:
            return "沒有音檔"
        return modify_sound_url(value.group())

    @pydantic.validator("dialect", "chinese_translation")
    @classmethod
    def has_content(cls, value: str) -> str:
        """The check_content method makes sure there is vocab or chinese translation value definied"""
        if value is None:
            return ""
        return value.text.strip()


@dataclass
class StoryCleaner(DataCleaner):
    """
    The StoryCleaner objects first extracts the data from the html, and then cleans it.
    """

    soup: BeautifulSoup

    def __post_init__(self) -> None:
        self.table_tag = self.soup.find("div", id="part_19")

    def remove_empty_dict(self, result: Generator) -> Generator[None, None, str]:
        """The remove_empty_dict method removes the dictionary with the empty value in each key.
        Args:
            result (map): the result after mapping `tr_lists` to the method `self.extract_data`.
        Returns:
            a generator.
        """
        return (story_dict for story_dict in result if story_dict.get("dialect") != "")

    def clean_data(self, specified_tag: BeautifulSoup) -> dict[str, str]:
        """The extract_data method extracts the data from the html.

        Args:
            specified_tag (BeautifulSoup): the specified html tag

        Returns:
            a dict: {
                'dialect': 'cingay balay qu pinqzywan nha’ squ ’ringan na matas qani.',
                'chinese_translation': '關於紋面的起源，眾說紛紜。',
                'sound_url': 'https://ilrdc.tw/grammar/sound/2/A3-2-1.mp3'}
            }
        """
        dialect = specified_tag.find(class_="ab")
        chinese_translation = specified_tag.find(class_="ch")
        sound_url = re.search('(?<=src\="\.).*(mp3|wav|ogg|wma)', str(specified_tag))
        data = StoryInfo(
            dialect=dialect,
            chinese_translation=chinese_translation,
            sound_url=sound_url,
        )
        return data.dict()

    def extract_data(self) -> Generator[None, None, dict]:
        tr_lists = self.table_tag.find_all("tr")
        result = map(self.clean_data, tr_lists)
        return self.remove_empty_dict(result)
