# Shitposter

Politely posts my latest blog entry to:

- slack
- twitter

## Usage

Set the `FEED_URL` environment variable (requried).

```
export FEED_URL="https://www.alexrecker.com/feed.xml"
```

### Slack

Set the `SLACK_WEBHOOK_URL` environment variable.

```
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
```

### Twitter

Twitter requires - not one - but _four_ different passwords just to post a friggen' tweet.  Good luck.

```
export TWITTER_CONSUMER_API_KEY="blah-blah"
export TWITTER_CONSUMER_API_SECRET_KEY="blah-blah"
export TWITTER_ACCESS_TOKEN="blah-blah"
export TWITTER_ACCESS_TOKEN_SECRET="blah-blah"
```

### Facebook

Just use your own credentials you coward.  I promise I won't steal them.

```
export FACEBOOK_LOGIN=me@buttholmail.org
export FACEBOOK_PASSWORD=my-password-that-ive-had-since-third-grade
```