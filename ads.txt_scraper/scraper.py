#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from collections import defaultdict
import eventlet
import requests
import datetime

eventlet.sleep()  # Fix for https://github.com/eventlet/eventlet/issues/401 in Debian

domains_file = "top-10000-sites.csv"
adstxt_entry = "kargo"
output_file = "output_file.txt"

with open(output_file, "w") as f:
    f.write(
        "Scraping for ads.txt in " + domains_file + " for " + adstxt_entry + " on " + datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S") + "\n")
    f.write("domain,ssp,in_ads_txt,date\n")
    print(
            "Scraping for ads.txt in " + domains_file + " for " + adstxt_entry + " on " + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S") + "\n")


def scrape_domains(input_domains):
    adstxt_headers = {
        "User-Agent": "AdsTxtCrawler/1.0; +https://github.com/InteractiveAdvertisingBureau/adstxtcrawler",
        "Accept": "text/plain",
    }

    columns = defaultdict(list)

    with open(input_domains) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                columns[k].append(v)

    for site in columns["URL"]:
        with open(output_file, "a") as f:
            with eventlet.Timeout(2):
                try:
                    r = requests.get(("http://" + site + "/ads.txt"), allow_redirects=1, headers=adstxt_headers,
                                     timeout=2)
                    if r.status_code == requests.codes.ok:
                        if adstxt_entry in r.content:
                            f.write(site + "," + adstxt_entry + "," + "yes" + "," + datetime.datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S") + "\n")
                            print(site + ": found " + adstxt_entry + ".")
                    else:
                        pass
                        f.write(site + "," + adstxt_entry + "," + "no" + "," + datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") + "\n")
                        print(site + ": nothing found.")

                except:
                    pass
                    f.write(site + "," + adstxt_entry + "," + "no" + "," + datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + "\n")
                    print(site + ": nothing found or error.")


scrape_domains(domains_file)
