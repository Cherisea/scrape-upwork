#!/usr/bin/python

import requests
import twitter
import config
from lxml import html

api = twitter.Api(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_KEY, config.ACCESS_SECRET)

min_budget = 1000

base_url = 'https://www.upwork.com'

# The page to scrape
page = requests.get('https://www.upwork.com/o/jobs/browse/c/web-mobile-software-dev/sc/web-development/t/1/?sort=create_time%2Bdesc')

tree = html.fromstring(page.content)

jobs = tree.cssselect('article')

for job in jobs:
    link = job.cssselect('h2 a')[0].get('href')
    name = job.cssselect('h2 a')[0].text_content().replace('\n', '').strip()
    budget = job.cssselect('.js-budget span')

    if len(budget) > 0:
        budget = budget[0].text_content().replace('\n', '').replace('$', '').replace(',', '').strip()

        try:
            budget = int(budget)
        except ValueError:
            budget = 0
    else:
        budget = 0

    if int(budget) > min_budget and name is not '':
        try:
            api.PostUpdate('($%s) %s - %s' % (budget, name, base_url + link))
        except Exception:
            # Just a duplicate tweet
            None

