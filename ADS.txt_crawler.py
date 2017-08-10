#!/usr/bin/python

import csv
import requests
import eventlet
eventlet.sleep() # Fix for https://github.com/eventlet/eventlet/issues/401 in Debian
from collections import defaultdict

eventlet.monkey_patch()

domain_source = 'https://moz.com/top500/domains/csv'
domains = "top_500_domains.csv"
output_file = "ads.txt"


def download_domains(domain_source):
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

    open(output_file, "w").close()
    for site in columns['URL']:
        try:
            with eventlet.Timeout(10):
                r = requests.get(("http://" + site + "ads.txt"), allow_redirects=1)
                print "Scraped " + r.url
                if (r.status_code == 200) and (r.headers['content-type'] == 'text/plain'):
                    with open(output_file, 'ab') as f:
                        f.write(r.url)
                        f.write("\n")
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
                                f.write("\n")
        except:
            print "Timed out scraping " + r.url
            pass


download_domains()
scrape_domains(domains)
