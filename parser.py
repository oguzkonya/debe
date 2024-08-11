from bs4 import BeautifulSoup as bs
from datetime import datetime
from debe import Debe
from entry import Entry
from entryprinter import Printer
from filter import Filter
from urllib.request import Request, urlopen
# import requests


TIMEOUT = 5
BASE_URL = "https://eksisozluk.com"
DEBE = BASE_URL + "/debe"
BIRI = BASE_URL + "/biri"
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0 '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    )
}

def fetch(url):
    result = None

    try:
        # browser = webdriver.Firefox()
        # browser.get(url)
        # html = browser.page_source
        # result = bs(html, features="html.parser")
        ## response = requests.get(url, timeout = (5, 10), headers = HEADERS)
        ## response.raise_for_status()
        ## result = bs(response.content, from_encoding=response.encoding, features="html.parser")
        req = Request(url, headers = HEADERS)
        webpage = urlopen(req).read()
        result = bs(webpage, features="html.parser")
    # except requests.exceptions.HTTPError as errh:
    #     print ("Http Error:", errh)
    # except requests.exceptions.ConnectionError as errc:
    #     print ("Connection Error:", errc)
    # except requests.exceptions.Timeout as errt:
    #     print ("Timeout Error:", errt)
    # except requests.exceptions.RequestException as err:
    #     print ("Error: ", err)
    except Exception as e:
        print ("Error: ", e)

    return result

def parseDebeList(filter):
    printer = Printer()
    bs = fetch(DEBE)
    debeList = []

    if bs is not None:
        try:
            entries = bs.find(id="partial-index").find_all("li")
            html = ""

            for entry in entries:
                debe = Debe()
                debe.link = entry.a["href"]
                debe.id = debe.link.replace("/entry/", "")
                debe.title = entry.a.span.string
                
                if filter.filterTitle(debe):
                    debeList.append(debe)

            nextDebe = None
            l = len(debeList)
            for i, debe in enumerate(debeList):
                if i < (l - 1):
                    nextDebe = debeList[i + 1]
                html += parseEntry(debe, nextDebe, printer)

            write(printer, html)
            
        except Exception as e:
            print(e)

def parseEntry(debe, nextDebe, printer):
    bs = fetch(BASE_URL + debe.link)

    if bs is not None:
        try:
            entry = Entry()
            entry.id = debe.id
            entry.nextId = nextDebe.id
            entry.title = debe.title
            entry.link = BASE_URL + debe.link
            entry.date = bs.find("a", {"class": "entry-date"}).text
            entry.author = bs.find("a", {"class": "entry-author"}).text
            entry.authorLink = BIRI + "/" + entry.author.replace(" ", "-")
            entry.content = bs.find("div", {"class": "content"}).decode_contents().replace('href="/?q=', 'href="' + BASE_URL + '/?q=').replace('href="/entry', 'href="' + BASE_URL + '/entry')

            return printer.printEntry(entry)

        except Exception as e:
            print(e)

def write(printer, html):
    contents = printer.printIndex(html, datetime.now().strftime("%d/%m/%Y"))

    g = open("index.html", "w")
    g.write(contents)
    g.close()

if __name__ == "__main__":
    f = Filter("filter.txt")
    parseDebeList(f)
