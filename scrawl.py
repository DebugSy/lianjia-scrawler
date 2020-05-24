from Queue import Queue
from threading import Thread

import core
import model
import settings
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)s - %(message)s', level=logging.INFO)


def get_communitylist(city):
    res = []
    for community in model.Community.select():
        if community.city == city:
            res.append(community.title)
    return res


def split_list_average_n(origin_list, n):
    if len(origin_list) > n:
        for i in range(0, len(origin_list), len(origin_list) // n):
            yield origin_list[i:i + n]
    else:
        yield origin_list



def main():
    queue = Queue()
    thread_list = []
    regionlist = settings.REGIONLIST  # only pinyin support
    city = settings.CITY
    model.database_init()
    # core.GetHouseByRegionlist(regionlist)
    # core.GetCommunityByRegionlist(city, regionlist)
    # communitylist = get_communitylist(city)  # Read celllist from database
    communitylist = settings.COMMUNITYLIST
    sub_communitylists = split_list_average_n(communitylist, 50)
    i = 0
    for sub_communitylist in sub_communitylists:
        thread = Thread(target=core.GetHouseByCommunitylist, name="Thread-" + str(i), args=(city, sub_communitylist,))
        # thread = Thread(target=core.GetSellByCommunitylist, name="Thread-" + str(i), args=(city, sub_communitylist,))
        thread.start()
        thread_list.append(thread)
        i += 1

    for t in thread_list:
        t.join()


if __name__ == "__main__":
    main()
