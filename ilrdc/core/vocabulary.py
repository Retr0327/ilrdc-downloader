import re
import pydantic
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Union, Any
from ilrdc.urldialector import URLDialector
from ilrdc.base import DataCleaner, DataDownloader
from ilrdc.util import modify_sound_url, download_url


class VocabularyInfo(pydantic.BaseModel):
    """
    The VocabularyInfo object keeps track of an item in inventory, including vocab, chinese translation and sound url.`
    """

    vocab: str
    chinese_translation: str
    sound_url: Any

    @pydantic.validator("sound_url")
    @classmethod
    def is_soud_url(cls, value) -> str:
        """The is_soud_url method makes sure there is sould_url value definied."""
        if value is None:
            return "沒有音檔"
        return modify_sound_url(value.group())

    @pydantic.validator("vocab", "chinese_translation")
    @classmethod
    def check_content(cls, value):
        """The check_content method makes sure there is vocab or chinese translation value definied"""
        if value is None:
            return "not found"
        return value


@dataclass
class VocabularyCleaner(DataCleaner):
    """
    The VocabularyCleaner objects first extracts the data from the html, and then cleans it.
    """

    soup: BeautifulSoup

    def __post_init__(self) -> None:
        self.table_tag = self.soup.find("table")

    def remove_alphabet_soup(
        self, tr_lists_with_alphabets: list[BeautifulSoup]
    ) -> list[BeautifulSoup]:
        """The remove_alphabet_soup method renives the soup object that contains English alphabet.

        Args:
            tr_lists_with_alphabets (list): the list of soup object

        Returns:
            a list
        """
        alphabet_soup = list(
            filter(
                None,
                [value.find("td", "alphabet") for value in tr_lists_with_alphabets],
            )
        )
        alphabet = list(map(lambda value: value.text, alphabet_soup))
        for bsObj in tr_lists_with_alphabets:
            if bsObj.text.strip() in alphabet:
                tr_lists_with_alphabets.remove(bsObj)
        return tr_lists_with_alphabets

    def clean_data(self, specified_tag: BeautifulSoup) -> dict[str, str]:
        """The extract_data method extracts the data from the html.

        Args:
            specified_tag (BeautifulSoup): the specified html tag

        Returns:
            a dict: {
                'dialect': 'aw',
                'chinese_translation': '好的；是的',
                'sound_url': 'https://ilrdc.tw/grammar/sound/2/A2-1-4.mp3'}
            }
        """
        vocab = specified_tag.find(class_="ab").text.strip()
        chinese_translation = specified_tag.find(class_="ch").text.strip()
        sound_url = re.search('(?<=src\="\.).*(mp3|wav|ogg|wma)', str(specified_tag))
        data = VocabularyInfo(
            vocab=vocab, chinese_translation=chinese_translation, sound_url=sound_url
        )
        return data.dict()

    def extract_data(self) -> map:
        tr_lists_with_alphabets = self.table_tag.find_all("tr")
        tr_lists = self.remove_alphabet_soup(tr_lists_with_alphabets)
        return map(self.clean_data, tr_lists)
