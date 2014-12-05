from unipath import Path
from crawl_exeter import run_spider
import logging

import nltk

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_fmt)

nltk.data.path.append('./data/')

def initialize_datasources():

    # If we don't have the right files, grab them.
    crawled_page = Path('./data/1.html')

    if not crawled_page.exists():
        logging.info("Crawling Exeter Book from en.wikisource.org")
        run_spider()
    else:
        logging.info("Crawled files in place")

    # If we don't have NLTK data, grab it.
    nltkdata_exists = Path('./data/tokenizers/punkt/english.pickle')

    if not nltkdata_exists.exists():
        logging.info("Downloading NLTK Data")
        nltk.download('punkt', './data')
    else:
        logging.info("NLTK Data in place")


if __name__ == "__main__":

    initialize_datasources()
