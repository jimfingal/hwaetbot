

To scrape the Exeter book, you can run:

	cd riddlescrape
	scrapy crawl exeter


Requires  buildpack:
	
	heroku config:add BUILDPACK_URL=git://github.com/heroku/heroku-buildpack-python.git

#  Python buildpack will install libffi for you if cffi or cryptography is present in your requirements.txt.