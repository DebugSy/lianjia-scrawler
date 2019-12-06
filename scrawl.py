import os
from Queue import Queue
from threading import Thread

import core
import model
import settings


def get_communitylist(city):
    res = []
    for community in model.Community.select():
        if community.city == city:
            res.append(community.title)
    return res


def split_list_average_n(origin_list, n):
    for i in range(0, len(origin_list), n):
        yield origin_list[i:i + n]


def main():
    queue = Queue()
    thread_list = []
    city = settings.CITY
    model.database_init()
    communitylist = settings.COMMUNITYLIST
    sub_communitylist = split_list_average_n(communitylist, 5)
    for _ in range(5):
        thread = Thread(target=core.GetHouseByCommunitylist, args=(city, sub_communitylist,))
        thread.start()
        thread_list.append(thread)

    for t in thread_list:
        t.join()

if __name__ == "__main__":
    main()
