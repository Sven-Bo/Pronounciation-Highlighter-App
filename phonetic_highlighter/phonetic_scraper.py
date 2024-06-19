import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def create_session():
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def word_exists(session, word):
    spellcheck_url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = session.get(spellcheck_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.content, "html.parser")
        if soup.find("h1", string="404. Page not found."):
            return False
        return True
    except requests.exceptions.RequestException:
        return False


def get_phonetics(word):
    session = create_session()

    if not word_exists(session, word):
        return None

    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.content, "html.parser")
        phonetics_span = soup.find("span", class_="ipa dipa lpr-2 lpl-1")
        if phonetics_span:
            return phonetics_span.text.strip()
        else:
            return None
    except requests.exceptions.HTTPError as http_err:
        return None
    except requests.exceptions.RequestException as err:
        return None
