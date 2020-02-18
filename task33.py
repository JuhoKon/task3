import json
import time
import requests
import argparse
from threading import Thread
from bs4 import BeautifulSoup
from collections import deque


def main_helper(start, end):
    '''
    Breadth-first search approach for shortest path between two Wikipedia pages.
    path is a dict of page (key): list of links from start to page (value).
    Q is a double-ended queue of pages to visit.
    '''
    path = {}
    path[start] = [start]
    Q = deque([start])

    links = get_links(Q[0])
    a = (round(len(links)/2))
    linksFirstPart = links[:a]
    linksSecondPart = links[a:]
    # print(links)

    t1 = Thread(target=find_shortest_path,
                args=((linksSecondPart), (Q), (start), (end))).start()
    t2 = Thread(target=find_shortest_path,
                args=((linksSecondPart), (Q), (start), (end))).start()
    #print((find_shortest_path(linksSecondPart, Q, start, end)))


def find_shortest_path(links, Q, start, end):

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
                return path[page] + [link]
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


def redirected(end):
    '''
    Returns the url that end page points to (helpful for end pages with redirected url)
    '''
    end_soup = BeautifulSoup(requests.get(end).content, 'html.parser')
    title = end_soup.find('h1').text
    title = title.replace(' ', '_', len(title))
    base_url = end[:end.find('/wiki/') + len('/wiki/')]
    return set([end, base_url + title])


def result(start, end, path):
    '''
    Returns json object of shortest path result.
    '''
    if path:
        result = path
    else:
        result = "No path! :( "
    d = {"start": start, "end": end, "path": result}
    return json.dumps(d, indent=4)


def main():
    '''
    Executes the WikiRacer for args (input arguments).
    '''

    start = "https://en.wikipedia.org/wiki/Malaria"
    end = "https://en.wikipedia.org/wiki/Microorganism"
    main_helper(start, end)
    # path = find_shortest_path(start, redirected(end))
    # json_result = result(start, end, path)
    # return json_result


if __name__ == '__main__':
    starttime = time.time()

    print(main())

    endtime = time.time()

    print(endtime - starttime)
