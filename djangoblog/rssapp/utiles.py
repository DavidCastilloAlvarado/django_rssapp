from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from .models import User_feed
import urllib3
import requests
http_poolmanag = urllib3.PoolManager()

retry_strategy = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


def get_rss_link(url):
    if not ("feed" in url or "rss" in url):
        response = http_poolmanag.request('GET', url)
        soup = BeautifulSoup(response.data, features='html.parser')
        rss_links = soup.select('link[type="application/rss+xml"]')
        # print(rss_links)
        rss_url = ""
        for link in rss_links:
            rss_url = link.get('href')
        if len(rss_url) > 0:
            return rss_url, True
        else:
            return rss_url, False
    else:
        return url, True


@ staticmethod
def get_items_from_feed(url, id, first, serializer, ** kwargs):
    """
    Get the items from the RSS provider, for every url we get the entries, 
    only the last 8. If the request fail, the event will be saved into the table
    log_errors
    """
    try:
        #response = requests.get(url)
        response = http.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")
        limit = 5 if first == 1 else 12
        items = soup.findAll('item', limit=limit)
        flag_entry = False
        if len(items) == 0:
            items = soup.findAll('entry', limit=limit)
            flag_entry = True

        if items is None:
            return []
        else:
            retrieve = []
            for item in get_feed(items, first):
                entry = dict(
                    title=item.title.text,
                    url=get_href(item.link) if flag_entry else item.link.text,
                    description=item.description if item.description is None else item.description.text,
                )
                # print(entry)
                retrieve.append(entry)
            return retrieve
    except:
        payload = dict(
            id_feed=id,
            url=url,
        )
        serializer_data = serializer(data=payload)
        if serializer_data.is_valid():
            serializer_data.save()
        return []


def get_href(link2):
    """
    Get the url in case is no posible to detect
    """
    link = str(link2)
    try:
        href = link.index("href=")
        link = link[(href+6):]
        end = link.index("\"")
        return link[:end]
    except:
        return link2.text


def get_feed(list, first):
    if first == 1:
        return list[:5]
    elif first == 0:
        return list[5:12]


def get_data_from_model(first, author, id_feed):
    if first == 1:
        return User_feed.objects.filter(author=author
                                        ).values_list("id", "url")
    elif first == 0:
        return User_feed.objects.filter(author=author,
                                        id=id_feed,
                                        ).values_list("id", "url")
