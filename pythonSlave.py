import json
import time
import requests
import argparse
from threading import Thread
from bs4 import BeautifulSoup
from collections import deque


def find_shortest_path(links, Q, start, end, return_dict, event):

    print(Q)
    i = 0
    path = {}
    path[start] = [start]

    while len(Q) != 0:
        # look at next page in queue of pages to visit, get wikilinks on that page
        page = Q[0]
        if i != 0:
            page = Q.popleft()
            links = get_links(page)
        i = 1
        # look at each link on the page
        for link in links:

            # if link is our destination, we're done!
            if link in end:
                print(path[page] + [link])
                return_dict["ass"] = path[page] + [link]
                event.set()
                return return_dict
            # if not, check if we already have a record of the shortest path from the start page to this link- if we don't, we need to record the path and add the link to our queue of pages to explore
            if (link not in path) and (link != page):
                path[link] = path[page] + [link]
                Q.append(link)

    # if we've exhausted all possible pages to explore in our queue without getting to the destination
    return None


def get_links(page):
    '''
    Retrieves distinct links in a Wikipedia page.
    '''
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')
    base_url = page[:page.find('/wiki/')]
    links = list({base_url + a['href']
                  for a in soup.select('p a[href]') if a['href'].startswith('/wiki/')})
    return links
