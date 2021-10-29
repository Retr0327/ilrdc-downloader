from abc import ABC, abstractmethod


class DataCleaner(ABC):
    """
    The DataCleaner objects cleans the data.
    """

    @abstractmethod
    def clean_data(self, specified_tag):
        """The clean_data method cleans the data from the BeautifulSoup object."""
        pass

    @abstractmethod
    def extract_data(self):
        """The extract_data method extracts the data from the BeautifulSoup object."""
        pass


class DataDownloader(ABC):
    @abstractmethod
    def get_data(self, info: dict):
        pass
    
    @abstractmethod
    def download(self):
        pass
