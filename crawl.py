import json
import logging

from bs4 import BeautifulSoup
from curl_cffi import requests

from resolve_challenge import ResolveChallenge

URL = "https://ocp.edu.in"

challenge_resolver = ResolveChallenge(URL, "hcdn")
headers = challenge_resolver.headers
cookies = challenge_resolver.post_challenge()
request = requests.Session()

visited_links = set()
results = list()
out = open("results.json", "a")

logger = logging.getLogger(__name__)
logging.basicConfig(filename='scrape.log', level=logging.INFO)
logger.info('Started')

def make_req(URL=URL, path="/", _type="get"):
    """
    this exists because its boring to use requests.get again and again \n
    returns response object
    """
    return requests.get(URL + path, cookies=cookies, headers=headers) if _type == "get" else  requests.post(URL + path, cookies=cookies, headers=headers)

def crawl_page(URL=URL):
    """
    crawl can be fatal, make sure to use it with limit 
    """
    page = BeautifulSoup(make_req(URL).text, "html.parser")
    elems = page.find_all(class_="fusion-bar-highlight", recursive=True)
    for elem in elems:
        link = elem.get('href')
        if link in visited_links:
            continue
        if link == "#":
            continue
        if URL not in link:
            continue
        main = get_main_content_from_page(link)
        logger.info(f"Got main content")
        results.append({"url": link, "short_text": elem.text, "text": main})
        visited_links.add(link)
        logger.info("going for next crawl")
        crawl_page(link)

def get_main_content_from_page(URL):
    page = BeautifulSoup(make_req(URL).text, "html.parser")
    main = page.find("main")
    if main is not None:
        return main.text
    return None # lol, idk i just wanted to

crawl_page()
out.write(json.dumps(results))
out.close()