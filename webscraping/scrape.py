import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pprint


session = requests.Session()
# Retry 3 times in case of requests.exceptions.ConnectionError
# backoff_factor will help to apply delays between attempts to avoid failing again in case of periodic request quota
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


all_pages_links = []
all_pages_subtext = []
for page in range(1,4): # Scrape the first 3 pages of Hacker News website
    try:
        res = session.get(f'https://news.ycombinator.com/news?p={page}')
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.titlelink')  # grab titlelink class
    subtext = soup.select('.subtext')  # grab subtext class
    all_pages_links.append(links)
    all_pages_subtext.append(subtext)

all_pages_links = [x for xs in all_pages_links for x in xs]
all_pages_subtext = [x for xs in all_pages_subtext for x in xs]


def sort_stories_by_votes(input_list):
    """Takes in a list and returns the sorted list by votes key in descending order"""
    return sorted(input_list, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    """Creates a list with stories that have more than 100 votes"""
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()  # grab title
        href = item.get('href', None)  # grab link (if exists)
        vote = subtext[idx].select('.score')  # grab score class
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))  # grab vote text, which is in the form "n points" in the score class
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


# Print a pretty version of the list with titles, links and votes of the first 3 pages of Hacker News website,
# taking into consideration only stories that have more than 100 votes
pprint.pprint(create_custom_hn(all_pages_links, all_pages_subtext))





