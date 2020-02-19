import json
import time
import requests
import argparse
from threading import Thread
from bs4 import BeautifulSoup
from collections import deque
from termcolor import colored
from multiprocessing import Process, Manager, Value


def find_shortest_path(links, Q, start, end, return_list, worker, run, path):
  # breadth-first search, first found entry is shortest
  # first process to find entry has the shortest based on the algorithm logic and that
  # each process gets the same resources
  # First process to find entry will stop other processes searching

  # Breadth-first search
  # https://en.wikipedia.org/wiki/Breadth-first_search
  # https://github.com/stong1108/WikiRacer/blob/master/wikiracer.py
    print(worker + " started. Finding shortest path...")
    i = 0

    page = start
    while (run.value):
        # look at next page in queue of pages to visit, get wikilinks from that page
        if i != 0:  # we are given list so at first iteration don't get new links
            page = Q.popleft()
            links = get_links(page)
        # look at each link on the page
        for link in links:
            if link == end:  # if found our destination
                # breadth first search so first entry is the shortest
                print(worker + " : " + colored("Found a way to our destination...",
                                               'green'))
                return_list.append(path[page] + [link])

                run.value = False
                # print(run)
                return return_list
            # if not, check if we already have a record of the shortest path from the start page to this link-
            # if we don't, we need to record the path and add the link to our queue of pages to explore
            if (link not in path) and (link != page):
                # add current path to searched page + this link
                path[link] = path[page] + [link]
                if i == 0:  # first iteration
                    Q.append(link)  # adds to right side
                    Q.popleft()  # pop left, has the [start] in it
                    i = 1  # conditional helper

                Q.append(link)

    print(worker + " returning.")
    return None


def get_links(page):
    if page == "https://en.wikipedia.org/wiki/Kosmoceratops":
        print("jeps")

    links = []
    request = requests.get(page)
    soup = BeautifulSoup(request.content, 'html.parser')
    baseUrl = "https://en.wikipedia.org"

    for link in soup.select('p a[href]'):  # select links
        if link['href'].startswith('/wiki/'):  # if link is valid
            links.append(baseUrl + link['href'])  # add to list

    return links
