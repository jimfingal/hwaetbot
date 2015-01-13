import os
from unipath import Path


data_path = Path('./data/')

REDIS_CORPUS = 'corpus'
REDIS_USED = 'used'
TWITTER_CHARLIMIT = 140

consumer_key = os.environ.get('HWAETBOT_CONSUMER_KEY')
consumer_secret = os.environ.get('HWAETBOT_CONSUMER_SECRET')
access_token = os.environ.get('HWAETBOT_ACCESS_TOKEN')
access_token_secret = os.environ.get('HWAETBOT_ACCESS_TOKEN_SECRET')

redis_url = os.getenv('HWAETBOT_REDIS_URL', 'redis://localhost:6379')
