import json
import time
import requests
import argparse
from threading import Thread
from bs4 import BeautifulSoup
from collections import deque
import pythonSlave
import multiprocessing
from multiprocessing import Process, Manager
import asyncio


def redirected(end):
    '''
    Returns the url that end page points to (helpful for end pages with redirected url)
    '''
    end_soup = BeautifulSoup(requests.get(end).content, 'html.parser')
    title = end_soup.find('h1').text
    title = title.replace(' ', '_', len(title))
    base_url = end[:end.find('/wiki/') + len('/wiki/')]
    return set([end, base_url + title])


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


def processes(linksFirstPart, linksSecondPart, linksThirdPart, linksFourthPart, linksFifthPart, Q, start, end, return_dict, event):
    p1 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksFirstPart, Q, start, redirected(end), return_dict, event))
    p1.start()

    p2 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksSecondPart, Q, start, redirected(end), return_dict, event))
    p2.start()

    p3 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksThirdPart, Q, start, redirected(end), return_dict, event))
    p3.start()

    p4 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksFourthPart, Q, start, redirected(end), return_dict, event))
    p4.start()

    p5 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksFifthPart, Q, start, redirected(end), return_dict, event))
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()


async def main():
    event = multiprocessing.Event()
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    start = "https://en.wikipedia.org/wiki/Airplane"
    end = "https://en.wikipedia.org/wiki/Car"
    path = {}
    path[start] = [start]
    Q = deque([start])

    links = get_links(Q[0])
    a = (round(len(links)/5))
    linksFirstPart = links[:a]
    linksSecondPart = links[a:2*a]
    linksThirdPart = links[2*a:3*a]
    linksFourthPart = links[3*a:4*a]
    linksFifthPart = links[4*a:]

    processes(linksFirstPart, linksSecondPart,
              linksThirdPart, linksFourthPart, linksFifthPart, Q, start, end, return_dict, event)

if __name__ == '__main__':
    starttime = time.time()

    asyncio.run(main())

    endtime = time.time()

    print(endtime - starttime)
