#!./venv/bin/python
import datetime
import logging
import os
import platform
import sys

import feedparser
import slack_sdk.webhook
import tweepy

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

    share_text = f'''
{latest['title']}
{latest['summary']}
{latest['link']}
    '''.strip()

    if slack := slack_client_from_env():
        slack.send(icon_emoji=':reckerbot:', text=share_text)
        logger.info('shared latest with slack')

    if twitter := twitter_client_from_env():
        twitter.update_status(status=share_text)
        logger.info('shared latest with twitter')

    end = datetime.datetime.now()
    logger.info('shitposter finished in %.2f', (end - start).total_seconds())


def slack_client_from_env():
    try:
        slack_sdk.webhook.WebhookClient(os.environ['SLACK_WEBHOOK_URL'])
    except KeyError:
        return None


def is_today(latest):
    latest_date = datetime.datetime.fromisoformat(latest['date'])
    todays_date = datetime.datetime.today()
    return latest_date.date() == todays_date.date()


def twitter_client_from_env():
    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key=os.environ['TWITTER_CONSUMER_API_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_API_SECRET_KEY'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        )
        return tweepy.API(auth)
    except KeyError:
        return None



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
