import json
import pandas as pd 
from functools import wraps
from typing import Optional, Union
from dataclasses import dataclass
from .urldialector import URLDialector
from .core import GrammarDownloader, VocabularyDownloader, StoryDownloader


# --------------------------------------------------------------------
# helper functions


def jsonify(dialect_ch: str, data: dict) -> None:
    """The jsonify function converts the argument `data` to a JSON file.
    Args:
        data (dict):
        dialect_ch (str): the dialect chinese name
    
    Returns:
        a json file
    """
    for key, value in data.items():
        with open(f"{dialect_ch} - {key}.json", "w", encoding="utf-8",) as file:
            json.dump(value, file, ensure_ascii=False)

def tablizer(dialect_ch: str, data: dict) -> None:
    """The tablizer method converts the argument `data` to a CSV file. If a dictionary has a key `Id`,
       the CSV file will contain columns with `Id`; if not, exclude `Id`.

    Args:
        data (dict):
        dialect_ch (str): the dialect chinese name

    Returns:
        a csv file
    """

    for key, value in data.items():
        df = pd.DataFrame(value)
        column = ["Id", "dialect", "chinese_translation", "sound_url"]
        if "Id" in value[0]:
            df = df[column]
        else:
            df = df[column[1:]]
        df.to_csv(
            f"{dialect_ch} - {key}.csv",
            index=False,
            encoding="utf_8_sig",
        )

def convert(datatype):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs): 
            data = self.download_data()
            if datatype == "json": 
                self.check_type(self.download_data(), jsonify)
            elif datatype == "csv":
                self.check_type(self.download_data(), tablizer)
        return wrapper
    return decorator 


# --------------------------------------------------------------------
# public interface


@dataclass
class ILRDC:
    """
    The ILRDC object downloads the data based on `dialect_ch`, `part_type` and `part`, and converts the data to 
    either a json or a csv file. 
    """
    
    dialect_ch: str
    part_type: str
    part: Optional[str] = None

    def __post_init__(self) -> None:
        self.dialector = URLDialector(self.dialect_ch, self.part)

    def download_data(self) -> Union[list[dict[str, str]], dict[str, str]]:
        """The download_data method downloads the data based on `self.part_type`.

        Returns:
            a dict if the `self.part` 
        """
        factories = {
            "grammar": GrammarDownloader(self.dialector),
            "vocab": VocabularyDownloader(self.dialector),
            "story": StoryDownloader(self.dialector),
        }
        return factories[self.part_type].download()
 
    def check_type(self, data, func):
        if isinstance(data, list):
            for value in data:
                if type(value) is dict: 
                    func(self.dialect_ch, value)
                else:
                    print(value)
        elif isinstance(data, dict):
            func(self.dialect_ch, data)
        else:
            return print(data)
    
    @convert('json')
    def to_json(self) -> None:
        """Convert the data to a json file"""
        return

    @convert('csv')  
    def to_csv(self) -> None:
        """Convert the data to a csv file"""
        return
