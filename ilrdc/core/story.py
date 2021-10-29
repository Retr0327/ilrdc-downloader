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


@dataclass
class StoryDownloader(DataDownloader):
    """
    The StoryDownloader object downloads the data in the story part.
    """

    url_dialector: URLDialector

    @property
    def request_info_list(self) -> Union[list[dict[str, str]], dict[str, str]]:
        """The request_info_list property set the request information list.

        Returns:
            a dict if a story part is specified, a list otherwise.
        """
        info_list = self.url_dialector.generate()
        if isinstance(info_list, list):
            return info_list[-1]
        return info_list

    def find_title_index(self, story_list: list) -> list[int]:
        """The find_title_index method finds the title, stored as a dictionary, from the argument `story_list`.

        Args:
            story_list (list): the story_list that comes from adding `self.story_request_info` to the method `self.download_content()'

        Returns:
            a list containing the title index in the argument `story_list`.
        """
        title_index = [
            num
            for num, story_dict in enumerate(story_list)
            if story_dict.get("sound_url") == "沒有音檔"
        ]
        final_index = len(story_list)
        title_index.append(final_index)
        return title_index

    def get_each_story(self, data: list) -> list[dict[str, str]]:
        """The get_each_story method finds each story from the argument `data`.

        Args:
            data (list): the data that comes from adding `self.story_request_info` to the method `self.download_content()'

        Returns:
            a list
        """
        title_index = self.find_title_index(data)
        index_num = 0
        stories_list = []
        while True:
            story = {
                data[title_index[index_num]].get("chinese_translation"): data[
                    title_index[index_num] + 1 : title_index[index_num + 1]
                ]
            }
            stories_list.append(story)
            index_num += 1
            if index_num == len(title_index) - 1:
                break
        return stories_list

    def extract_story_data(self, url: str) -> map:
        """The extract_story_data method extracts the story data based on the argument `url`.

        Args:
            url (str): the story url

        Returns:
            a map object
        """
        bsObj = download_url(url)
        return StoryCleaner(bsObj).extract_data()

    def get_data(self, info: dict) -> Union[dict[str, str], str]:
        """The get_data method gets the data from the argument `info`.

        Args:
            info (dict): the request info in `self.request_info_list`

        Returns:
            a dict if the `story_data` is not an empty list, a string otherwise
        """
        url = info["part_url"]
        part = info["part_name"]
        story_data = list(self.extract_story_data(url))
        if story_data:
            return story_data

        return f"沒有「{part}」相關資料"

    def download(self) -> dict[str, list]:
        """The download method downloads the data by mapping `self.request_info_list` into the method `get_data`.

        Returns:
            a dict
        """
        result = self.get_data(self.request_info_list)
        stories = self.get_each_story(result)
        return stories
