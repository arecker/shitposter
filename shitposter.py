#!./venv/bin/python
import collections
import datetime
import logging
import os
import platform
import sys
import time

import feedparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
    if not is_today(latest) and not should_force_publish():
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

    if facebook := facebook_creds_from_env():
        post_on_facebook(creds=facebook, share_text=share_text)
        logger.info('shared latest on facebook')

    end = datetime.datetime.now()
    logger.info('shitposter finished in %.2f', (end - start).total_seconds())


def slack_client_from_env():
    try:
        slack_sdk.webhook.WebhookClient(os.environ['SLACK_WEBHOOK_URL'])
    except KeyError:
        return None


def should_force_publish():
    return os.environ.get('FORCE_PUBLISH', '').lower() in ('true', '1', 'yas')


def is_today(latest):
    latest_date = datetime.datetime.fromisoformat(latest['date'])
    todays_date = datetime.datetime.today()
    return latest_date.date() == todays_date.date()


FacebookCreds = collections.namedtuple('FacebookCreds', 'login password')


def facebook_creds_from_env() -> FacebookCreds:
    try:
        return FacebookCreds(login=os.environ['FACEBOOK_LOGIN'], password=os.environ['FACEBOOK_PASSWORD'])
    except KeyError:
        return None


def post_on_facebook(creds=None, share_text=''):
    os.environ['MOZ_HEADLESS'] = 'true'
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get('https://m.facebook.com')
    logger.info('facebook - launched browser')
    time.sleep(2)
    elem = driver.find_element(By.ID, 'm_login_email')
    elem.clear()
    elem.send_keys(creds.login)
    elem = driver.find_element(By.ID, 'm_login_password')
    elem.clear()
    elem.send_keys(creds.password)
    driver.find_element(By.XPATH, "//button[@value='Log in']").click()
    logger.info('facebook - logged in with credentials')
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[contains(text(), 'Not now')]").find_element(By.XPATH, "../.").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[contains(text(), 'on your mind?')]").click()
    time.sleep(2)
    elem = driver.find_element(By.XPATH, "//textarea[@aria-label=\"What's on your mind?\"]")
    elem.clear()
    elem.send_keys(share_text)
    driver.find_element(By.XPATH, "//button[@value='Post'][contains(text(), 'Post')]").click()
    logger.info('facebook - submitted new post')


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
