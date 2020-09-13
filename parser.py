from bs4 import BeautifulSoup as bs
from debe import Debe
from filter import Filter
import requests


TIMEOUT = 5
BASE_URL = "https://eksisozluk.com"
URL = BASE_URL + "/debe"
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    )
}

def fetch(url):
    result = None

    try:
        response = requests.get(url, timeout=TIMEOUT, headers = HEADERS)
        response.raise_for_status()
        result = bs(response.content, from_encoding=response.encoding, features="html.parser")
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Connection Error:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("Error: ", err)

    return result

def parseDebeList(filter):
    bs = fetch(URL)
    debeList = []

    if bs is not None:
        try:
            entries = bs.find(id="content-body").find_all("li")

            for entry in entries:
                debe = Debe()
                debe.link = entry.a["href"]
                debe.title = entry.a.span.string
                
                if filter.filterTitle(debe):
                    debeList.append(debe)

            for debe in debeList:
                parseEntry(debe)

        except Exception as e:
            print(e)

def parseEntry(debe):
    bs = fetch(BASE_URL + debe.link)

    if bs is not None:
        try:
            contents = bs.find("div", {"class": "content"}).decode_contents()
            date = bs.find("a", {"class": "entry-date"}).text
            author = bs.find("a", {"class": "entry-author"}).text

            # TODO: Put these in an html file

        except Exception as e:
            print(e)

if __name__ == "__main__":
    f = Filter("filter.txt")
    parseDebeList(f)
