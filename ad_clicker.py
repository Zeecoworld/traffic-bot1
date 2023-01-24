import random
from argparse import ArgumentParser
from time import sleep
from config import logger, update_log_formats
import random
from proxy import get_proxies
from utils import create_webdriver
from search_controller import SearchController
import requests
from proxynova_scraper import get_proxies
from proxy_checking import ProxyChecker


__author__ = "Coşkun Deniz <coskun.denize@gmail.com>"

def scraping_proxy():
    proxies = get_proxies()
    for p in proxies:
        # print(p["proxyIp"] +":"+ p["proxyPort"])
        re = p["proxyIp"] +":"+ p["proxyPort"]
    return re

def tested_proxy():
    scrapped_proxy = scraping_proxy()
    checker = ProxyChecker()
    tested_proxy_ip  = checker.check_proxy(scrapped_proxy)
    return tested_proxy_ip["status"]




def get_arg_parser() -> ArgumentParser:
    """Get argument parser

    :rtype: ArgumentParser
    :returns: ArgumentParser object
    """

    arg_parser = ArgumentParser()
    # arg_parser.add_argument("-q", "--query", help="Search query")
    # arg_parser.add_argument(
    #     "-t",
    #     "--visittime",
    #     default=4,
    #     type=int,
    #     dest="ad_visit_time",
    #     help="Number of seconds to wait on the ad page opened",
    # )
    arg_parser.add_argument("--headless", action="store_true", help="Use headless browser")
    arg_parser.add_argument(
        "-p",
        "--proxy",
        help="""Use the given proxy in "ip:port" or "username:password@host:port" format""",
    )
    arg_parser.add_argument(
        "-pf",
        "--proxy_file",
        help="Select a proxy from the given file",
    )
    # arg_parser.add_argument(
    #     "--auth",
    #     action="store_true",
    #     help="""Use proxy with username and password.
    #     If this is passed, proxy parameter should be in "username:password@host:port" format
    #     """,
    # )
    arg_parser.add_argument("--id", help="Browser id for multiprocess run")

    return arg_parser


def main():
    """Entry point for the tool"""
    proxy = None
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    if args.id:
        update_log_formats(args.id)

    # if not args.query:
    #     logger.error("Run with search query!")
    #     arg_parser.print_help()
    #     raise SystemExit()

    if args.proxy:
        proxy = args.proxy
    elif args.proxy_file:
        proxies = get_proxies(args.proxy_file)
        logger.debug(f"Proxies: {proxies}")

        proxy = random.choice(proxies)
    else:
        result = tested_proxy()
        if result == True:
           proxy = scraping_proxy()   ###TESTING THE PROXIES HERE.....
        else:
            proxy = None

    driver = create_webdriver(proxy,False,True)

    search_controller = SearchController(driver,ad_visit_time=5)
    ads = search_controller.search_for_ads()

    if not ads:
        logger.info("No ads in the search results!")
    else:
         search_controller.click_ads(ads)
         search_controller.end_search()
        #  video = driver.find_element_by_id('movie_player')
        #  video.send_keys(Keys.SPACE) #hits space
    


if __name__ == "__main__":
  while True:
       main()
       sleep(random.choice([0.5, 1.5, 2, 2.5, 3]))
       

