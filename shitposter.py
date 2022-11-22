#!./venv/bin/python
import datetime
import logging
import os
import platform
import sys

import feedparser
import slack_sdk.webhook

logger = logging.getLogger(__name__)


def main():
    start = datetime.datetime.now()
    logger.info('starting shitposter with python v%s (%s)', platform.python_version(), sys.executable)

    if 'FEED_URL' not in os.environ:
        logger.fatal('FEED_URL="..." is not set!')
        sys.exit(1)

    latest = feedparser.parse(os.environ['FEED_URL']).entries[0]
    logger.info('found latest entry %s', latest['title'])
    if not is_today(latest):
        logger.info('latest entry is old, nothing to do')
        sys.exit(0)

    if webhook_url := os.environ.get('SLACK_WEBHOOK_URL'):
        post_slack(latest, webhook_url)

    end = datetime.datetime.now()
    logger.info('shitposter finished in %.2f', (end - start).total_seconds())


def post_slack(latest, webhook_url):
    webhook = slack_sdk.webhook.WebhookClient(webhook_url)
    webhook.send(icon_emoji=':reckerbot:', text=f'''
{latest['title']}
{latest['summary']}
{latest['link']}'''.strip())


def is_today(latest):
    latest_date = datetime.datetime.fromisoformat(latest['date'])
    todays_date = datetime.datetime.today()
    return latest_date.date() == todays_date.date()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
