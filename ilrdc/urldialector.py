from enum import Enum
from urllib.parse import urljoin
from dataclasses import dataclass, field


BASE_URL = "http://ilrdc.tw/grammar/"

# --------------------------------------------------------------------
# enum classes


class ILRDCComponent(Enum):
    """
    The ILRDCComponent object stores the information of a ILRDC component.
    """

    @classmethod
    def get_dict_info(cls) -> dict[str, str]:
        """The get_info_dict class method makes a dict from an enum.

        Returns:
            a dict
        """
        return dict(map(lambda item: (item.name, item.value), cls))

    @classmethod
    def get_list_info(cls) -> list[str]:
        """The get_info class method makes a list from an enum.

        Returns:
            a list
        """
        return list(map(lambda item: (item.name), cls))


class ILRDCDialect(ILRDCComponent):
    泰雅語 = 2
    邵語 = 4
    賽德克語 = 5
    布農語 = 6
    魯凱語 = 8
    噶瑪蘭語 = 10
    卑南語 = 12
    雅美語 = 13
    撒奇萊雅語 = 14
    卡那卡那富語 = 15


class ILRDCPart(ILRDCComponent):
    詞彙與構詞 = 3
    基本句型及詞序 = 4
    格謂標記與代名詞系統 = 5
    焦點與時貌語氣系統 = 6
    存在句所有句方位句結構 = 7
    祈使句結構 = 8
    使動結構 = 9
    否定句結構 = 10
    疑問句結構 = 11
    連動結構 = 12
    補語結構 = 13
    修飾結構 = 14
    並列結構 = 15
    其他結構 = 16
    標點符號 = 17
    基本詞彙 = 18
    長篇語料 = 19


# --------------------------------------------------------------------
# helper classes or functions


@dataclass
class URLCreator:
    """
    The URLCreator object converts the given dialecdt name to its corresponding url.
    """

    dialect_ch: str
    dialect_id: str = field(init=False, default_factory=str)

    def __post_init__(self) -> None:
        self.dialect_id = ILRDCDialect[self.dialect_ch].value
        self.list_of_part_ids = list(map(lambda part: part.value, ILRDCPart))

    def combine_to_url(self, part_id: str) -> str:
        """The combine_to_url method combines a part id with the dialect id to an url.

        Args:
            part_id (str): the part id

        Returns:
            a str: a url (e.g. http://ilrdc.tw/grammar/index.php?l=2&p=3)
        """
        return urljoin(BASE_URL, f"index.php?l={self.dialect_id}&p={part_id}")

    def create(self) -> list[str]:
        """The create method creates a list of urls.

        Returns:
            a list
        """
        urls = map(self.combine_to_url, self.list_of_part_ids)
        return list(urls)
