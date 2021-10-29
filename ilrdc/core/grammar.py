import re
import pydantic
from typing import Union
from bs4 import BeautifulSoup
from dataclasses import dataclass
from ilrdc.urldialector import URLDialector
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

    @pydantic.validator("Id", "dialect", "chinese_translation")
    @classmethod
    def check_content(cls, value):
        """The check_content method makes sure there is Id, dialect or chinese translation value definied"""
        if value is None:
            return "not found"
        return value


@dataclass
class GrammarCleaner(DataCleaner):
    """
    The GrammarCleaner objects first extracts the data from the html, and then cleans it.
    """

    soup: BeautifulSoup

    def __post_init__(self) -> None:
        self.table_tag = self.soup.find(class_="template-1")

    def clean_data(self, specified_tag: BeautifulSoup) -> dict[str, str]:
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


@dataclass
class GrammarDownloader(DataDownloader):
    """
    The GrammarDownloader object downloads the data in the grammar part.
    """

    url_dialector: URLDialector

    @property
    def request_info_list(self) -> Union[list[dict[str, str]], dict[str, str]]:
        """The request_info_list property set the request information list.

        Returns:
            a dict if a grammar part is specified, a list otherwise.
        """
        info_list = self.url_dialector.generate()
        if isinstance(info_list, list):
            return info_list[:-2]
        return info_list

    def extract_grammar_data(self, url: str) -> map:
        """The extract_grammar_data method extracts the grammar data based on the argument `url`.

        Args:
            url (str): the grammar url

        Returns:
            a map object
        """
        bsObj = download_url(url)
        return GrammarCleaner(bsObj).extract_data()

    def get_data(self, info: dict) -> Union[dict[str, str], str]:
        """The get_data method gets the data from the argument `info`.

        Args:
            info (dict): the request info in `self.request_info_list`

        Returns:
            a dict if the `grammar_data` is not an empty list, a string otherwise
        """
        url = info["part_url"]
        part = info["part_name"]
        grammar_data = list(self.extract_grammar_data(url))
        if grammar_data:
            return {part: grammar_data}

        return f"沒有「{part}」相關資料"

    def download(self) -> Union[dict[str, str], list[dict[str, str]]]:
        """The download method downloads the data by mapping `self.request_info_list` into the method `get_data`.

        Returns:
            a dict if the `self.request_info_list` is not a list, a list otherwise.
        """
        if isinstance(self.request_info_list, dict):
            return self.get_data(self.request_info_list)
        return list(map(self.get_data, self.request_info_list))
