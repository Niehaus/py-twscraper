import json
import os
from pprint import pprint

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

            # print(tweet.retweetedTweet)
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
            mentioned_users = data['mentionedUsers']
            quoted_tweet = data['quotedTweet']

            mentions = mentions_in_tweet(mentioned_users)
            who_was_rt, is_rt = is_retweet(quoted_tweet)

            tweet_info = {
                'Id': data['id'],
                'Label': username,
                'link': f'https://twitter.com/{username}',
                'content': data['renderedContent'],
                'mentioned_users': ' '.join(mentions),
                'verified': verified,
                'is_rt': is_rt,
                'who_was_rt': who_was_rt
            }
            scraped_tweets.append(tweet_info)

        scraped_file.close()
        os.remove("tmp_file.json")

        return scraped_tweets


class Iramuteq:

    @staticmethod
    def iramuteq_data_processor(content, variables):
        ...


class Gephi:

    def __init__(self, scraped_tweets):
        self.tweets = scraped_tweets
        self.graph = GephiData()

    def create_nw_mentions_rts(self):
        for tweet in self.tweets:
            if not self.graph.node_exists(tweet):
                # pprint(tweet)
                self.create_node(tweet)
                self.create_nodes_mentions(tweet['mentioned_users'])
        pprint(self.graph.nodes)
        self.create_edge(self.tweets[0], self.tweets[1])
        # pprint(self.graph.edges)

    def create_edge(self, source, target, label=0):
        edge = {
            'Source': source['Id'],
            'Target': target['Id'],
            'Type': 'Directed',
            'Label': label,
            'timeset': '',
            'Weight': 1
        }

        self.graph.edges.append(edge)

    def create_node(self, tweet):
        node = {
            'Id': tweet['Id'],
            'Label': tweet['Label'],
            'link': tweet['link'],
            'verified': tweet['verified']
        }

        self.graph.nodes.append(node)

    def create_nodes_mentions(self, mentions):
        if mentions != 'None':
            mentions_list = mentions.split(' ')
            for mention in mentions_list:
                node_info = get_user_info(mention)
                self.create_node(node_info)
                # não esquecer de criar uma aresta entre o nó que mencionou who_mentioned


class GephiData:

    def __init__(self):
        self.nodes = []
        self.edges = []

    def node_exists(self, tweet):
        for node in self.nodes:
            if tweet['Id'] == node['Id']:
                return True
            return False


# Aux methods to get specific tweet info
def is_retweet(quoted_tweet):
    if quoted_tweet is not None:
        return quoted_tweet['user']['username'], True  # username, is_rt bool
    return None, False


def mentions_in_tweet(mentioned_users):
    mentions = []
    if mentioned_users is not None:
        for user in mentioned_users:
            mentions.append(user['username'])
    else:
        mentions.append('None')

    return mentions


def get_user_info(username):
    user = sntwitter.TwitterUserScraper(username).entity
    user_info = {
        'Id': user.id,
        'Label': user.username,
        'link': f'https://twitter.com/{user.username}',
        'verified': user.verified,
        'followersCount': user.followersCount
    }

    return user_info
