import logging

import nltk
import redis
from unipath import Path


import hwaetbot.config as config
from hwaetbot.riddle_parser import parse_corpus
from hwaetbot.crawler import run_spider


def initialize_datasources(redis_client):

    boostrap_nltk()

    # Initialize corpus in Redis
    if not len(redis_client.smembers(config.REDIS_CORPUS)):
        logging.info("No riddles in db, parsing files")

        boostrap_crawled_files()

        sentences = parse_corpus()

        for sentence in sentences:
            redis_client.sadd(config.REDIS_CORPUS, sentence)


def boostrap_nltk():
    # If we don't have NLTK data, grab it.
    nltk.data.path.append('./data/')
    nltkdata_exists = Path('./data/tokenizers/punkt/english.pickle')

    if not nltkdata_exists.exists():
        logging.info("Downloading NLTK Data")
        nltk.download('punkt', './data')


def boostrap_crawled_files():
    # If we don't have the right files, grab them.
    crawled_page = Path('./data/1.html')

    if not crawled_page.exists():
        logging.info("Crawling Exeter Book from en.wikisource.org")
        run_spider()
    else:
        logging.info("Crawled files in place")




if __name__ == "__main__":

    redis_client = redis.from_url(config.redis_url)
    initialize_datasources(redis_client)