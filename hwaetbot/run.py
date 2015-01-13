import logging
import redis

from tweet_generator import TweetGenerator, fake_anglo_saxon_meter, write_tweet
import hwaetbot.config as config
from hwaetbot.bootstrap import initialize_datasources

log_fmt = "%(levelname)-6s %(processName)s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)
    

def generate_and_send_tweet(redis_client):
    without_meter, with_meter = get_tweet_with_meter(redis_client)

    logging.info("Generated Tweet ::\n%s " % without_meter)
    logging.info("With Meter :: \n%s" % with_meter)

    write_tweet(with_meter)

    redis_client.sadd(config.REDIS_USED, without_meter)
    redis_client.save()

def get_tweet_with_meter(redis_client):

    corpus = redis_client.smembers(config.REDIS_CORPUS)
    tg = TweetGenerator(corpus, 3) # Trigrams

    without_meter = None
    with_meter = None

    while True:
        
        without_meter = tg.generate_tweet()

        if redis_client.sismember(config.REDIS_USED, without_meter):
            logging.debug("Already used tweet :: %s" % without_meter)
            continue

        with_meter = fake_anglo_saxon_meter(without_meter)

        if len(with_meter) <= config.TWITTER_CHARLIMIT: 
            break

    return without_meter, with_meter


if __name__ == "__main__":

    redis_client = redis.from_url(config.redis_url)

    initialize_datasources(redis_client)
    generate_and_send_tweet(redis_client)

    