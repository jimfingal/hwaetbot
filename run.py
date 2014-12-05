from unipath import Path
from tweet_generator import TweetGenerator, fake_anglo_saxon_meter
import logging


import redis
import os

REDIS_CORPUS = 'corpus'
REDIS_USED = 'used'
TWITTER_CHARLIMIT = 140

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_fmt)


def _boostrap_crawled_files():
    # If we don't have the right files, grab them.
    crawled_page = Path('./data/1.html')

    if not crawled_page.exists():
        logging.info("Crawling Exeter Book from en.wikisource.org")
        from crawl_exeter import run_spider
        run_spider()
    else:
        logging.info("Crawled files in place")

def _boostrap_nltk():
    # If we don't have NLTK data, grab it.
    nltkdata_exists = Path('./data/tokenizers/punkt/english.pickle')

    if not nltkdata_exists.exists():
        logging.info("Downloading NLTK Data")
        import nltk
        nltk.download('punkt', './data')

def initialize_datasources(r):

    _boostrap_nltk()

    # Initialize corpus in Redis
    if not len(r.smembers(REDIS_CORPUS)):
        _boostrap_crawled_files()

        from parse_riddles import parse_corpus

        sentences = parse_corpus()

        for sentence in sentences:
            r.sadd(REDIS_CORPUS, sentence)
    

def get_tweet_with_meter(r):

    corpus = r.smembers(REDIS_CORPUS)
    tg = TweetGenerator(corpus, 3) # Trigrams

    without_meter = None
    with_meter = None

    used = r.smembers(REDIS_USED)

    logging.debug("Used already: %s" % used)

    while True:
        
        without_meter = tg.generate_tweet()

        if without_meter in used:
            continue

        with_meter = fake_anglo_saxon_meter(without_meter)

        if len(with_meter) <= TWITTER_CHARLIMIT: 
            break

    return without_meter, with_meter

if __name__ == "__main__":

    redis_url = os.getenv('HWAETBOT_REDIS_URL', 'redis://localhost:6379')
    r = redis.from_url(redis_url)

    initialize_datasources(r)

    without_meter, with_meter = get_tweet_with_meter(r)

    logging.info("Generated Tweet ::\n%s " % without_meter)
    logging.info("With Meter :: \n%s" % with_meter)

    r.sadd(REDIS_USED, without_meter)

    # Blocking, synchronous save. Only we use redis and we want it to be maximally persistent.
    r.save()