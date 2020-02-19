import json
import time
import requests
import argparse
from threading import Thread
from bs4 import BeautifulSoup
from collections import deque
import pythonSlave
import multiprocessing
from multiprocessing import Process, Manager, Value
import asyncio
from termcolor import colored


def processes(linksFirstPart, linksSecondPart, linksThirdPart, linksFourthPart, linksFifthPart, Q, start, end, return_list, run, path):
    p1 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksFirstPart, Q, start,
                       end, return_list, 'Worker 1', run, path))
    p1.start()

    p2 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksSecondPart, Q, start,
                       end, return_list, 'Worker 2', run, path))
    p2.start()

    p3 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksThirdPart, Q, start,
                       end, return_list, 'Worker 3', run, path))
    p3.start()

    p4 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksFourthPart, Q, start,
                       end, return_list, 'Worker 4', run, path))
    p4.start()

    p5 = Process(target=pythonSlave.find_shortest_path,
                 args=(linksFifthPart, Q, start,
                       end, return_list, 'Worker 5', run, path))
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()


def printHelper(return_list, totalTime):
    shortest = 9999999
    shortestEntry = {}
    helper = 1

    for a in return_list:  # processes outputs
        if (len(a) < shortest):
            shortest = len(a)
            shortestEntry = a

    print("\nFound a way from: " +
          colored(str(shortestEntry[0]), 'blue') + " to: " + colored(str(shortestEntry[shortest-1]), 'blue') + " with " + str(shortest-2) + " pages between.")

    print(colored("\nShortest route: \n", 'blue', attrs=['bold']))

    for page in shortestEntry:
        print(colored(str(helper) + ": "+str(page), 'cyan'))
        helper += 1
    print(colored("\nTotal time taken: " +
                  str(round(totalTime, 2)) + " seconds.", 'green'))


def main(start, end):
    #run = Value('i', True)
    manager = multiprocessing.Manager()
    return_list = manager.list()
    run = manager.Value('i', True)
    # print(run)
    path = manager.dict()
    path[start] = [start]
    Q = deque([start])

    links = pythonSlave.get_links(Q[0])
    a = (round(len(links)/5))
    linksFirstPart = links[:a]
    linksSecondPart = links[a:2*a]
    linksThirdPart = links[2*a:3*a]
    linksFourthPart = links[3*a:4*a]
    linksFifthPart = links[4*a:]
    Q = deque(
        [start])

    # start shit
    starttime = time.time()
    processes(linksFirstPart, linksSecondPart,
              linksThirdPart, linksFourthPart, linksFifthPart, Q, start, end, return_list, run, path)
    endtime = time.time()
    totalTime = endtime-starttime
    printHelper(return_list, totalTime)


def main2(start, end):

    manager = multiprocessing.Manager()
    return_list = manager.list()
    run = manager.Value('i', True)
    path = manager.dict()
    path[start] = [start]

    Q = deque([start])

    links = pythonSlave.get_links(Q[0])

    starttime = time.time()
    p1 = Process(target=pythonSlave.find_shortest_path,
                 args=(links, Q, start, end, return_list, 'Only 1 worker', run, path))
    p1.start()
    p1.join()
    endtime = time.time()
    totalTime = endtime-starttime
    printHelper(return_list, totalTime)


if __name__ == '__main__':

    start = "https://en.wikipedia.org/wiki/Airplane"
    end = "https://en.wikipedia.org/wiki/Royal_Air_Force"
    main(start, end)
    main2(start, end)
