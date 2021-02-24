import json
import os

import snscrape.modules.twitter as sntwitter


class Scraper:

    @staticmethod
    def api_scrape_tweets_by_content(since_date, until_date, keyword, max_tweets):
        scraped_tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
                keyword + f' since:{since_date} '
                          f'until:{until_date} '
                          f'-filter:links '
                          f'-filter:nativeretweets '
        ).get_items()):
            mentions = []
            if tweet.mentionedUsers is not None:
                for mentionedUser in tweet.mentionedUsers:
                    mentions.append(mentionedUser.username)

            is_rt = False
            who_was_rt = None
            if tweet.quotedTweet is not None:
                who_was_rt = tweet.quotedTweet.username
                is_rt = True

            row_tweet = {
                'Id': tweet.id,
                'Label': tweet.user.username,
                'link': f'https://twitter.com/{tweet.user.username}',
                'content': tweet.renderedContent,
                'mentioned_users': ' '.join(mentions),
                'verified': tweet.user.verified,
                'is_rt': is_rt,
                'who_was_rt': who_was_rt
            }

            scraped_tweets.append(row_tweet)
            if i > max_tweets:
                break

        return scraped_tweets

    @staticmethod
    def cli_scrape_tweets_by_content(since_date, until_date, keyword, max_tweets):
        os.system(f'snscrape '
                  f'--jsonl '
                  f'--max-results {max_tweets} '
                  f'twitter-search "{keyword} since:{since_date} until:{until_date}"'
                  f' > tmp_file.json')

        scraped_file = open('tmp_file.json')
        scraped_tweets = []
        for user_tweet in scraped_file:
            data = json.loads(user_tweet)

            username = data['user']['username']
            verified = data['user']['verified']
            protected = data['user']['protected']
            followers = data['user']['followersCount']
            mentioned_users = data['mentionedUsers']
            quoted_tweet = data['quotedTweet']


            mentions = mentions_in_tweet(mentioned_users)
            quoted_tweet, is_rt = is_retweet(quoted_tweet)

            tweet_info = {
                'Id': data['id'],
                'Label': username,
                'link': f'https://twitter.com/{username}',
                'followers': followers,
                'content': data['renderedContent'],
                'mentioned_users': ' '.join(mentions),
                'verified': verified,
                'protected': protected,
                'is_rt': is_rt,
                'who_was_rt': quoted_tweet['who_was_rt'],
                'content_of_rt': quoted_tweet['rt_content'],
                'rt_id': quoted_tweet['rt_id']
            }
            scraped_tweets.append(tweet_info)

        scraped_file.close()
        os.remove("tmp_file.json")

        return scraped_tweets


# Aux methods to get specific tweet info
def is_retweet(quoted_tweet):
    if quoted_tweet is not None:
        qt_info = {
            'who_was_rt': quoted_tweet['user']['username'],
            'rt_content': quoted_tweet['content'],
            'rt_id': quoted_tweet['id']
        }
        return qt_info, True  # quoted tweet info, is_rt bool
    else:
        qt_info = {
            'who_was_rt': None,
            'rt_content': None,
            'rt_id': None
        }
        return qt_info, False


def mentions_in_tweet(mentioned_users):
    mentions = []
    if mentioned_users is not None:
        for user in mentioned_users:
            mentions.append(user['username'])
    else:
        mentions.append('No Mentions')
    mentions = remove_duplicates(mentions)

    return mentions


def remove_duplicates(mylist):
    return list(dict.fromkeys(mylist))
