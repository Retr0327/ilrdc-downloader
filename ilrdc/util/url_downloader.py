import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def download_url(url: str) -> BeautifulSoup:
    """The download_url function downloads the url.

    Args:
        url (str): the url

    Returns:
        a BeautifulSoup object
    """
    req = requests.get(url, headers={"user-agent": UserAgent().google})
    soup = BeautifulSoup(req.text, "lxml")
    return soup
