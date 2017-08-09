#!/usr/bin/python
# Working on an implementation that's better than the IAB one because that one, while it lays out each piece of functionality, breaks whenever a site returns funky stuff.

import csv
import requests
import eventlet
from collections import defaultdict

eventlet.monkey_patch()

domain_source = 'https://moz.com/top500/domains/csv'
domains = "top_500_domains.csv"


def download_domains():
    print "Downloading Source Domains"
    r = requests.get(domain_source)
    with open(domains, "wb") as code:
        code.write(r.content)


def scrape_domains(input_domains):
    columns = defaultdict(list)
    with open(input_domains) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                columns[k].append(v)

    for site in columns['URL']:
        try:
            with eventlet.Timeout(10):
                r = requests.get(("http://" + site + "ads.txt"), allow_redirects=1)
                if (r.status_code == 200) and (r.headers['content-type'] == 'text/plain'):
                    print r.url + "\n", r.content
                    # print site + "ads.txt"
        except:
            pass


download_domains()
scrape_domains(domains)
