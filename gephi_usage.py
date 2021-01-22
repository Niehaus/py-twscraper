from pprint import pprint

import snscrape.modules.twitter as sntwitter


class Gephi:

    def __init__(self, scraped_tweets):
        self.tweets = scraped_tweets
        self.used_ids = []
        self.graph = GephiData()

    def graph_of_mentions(self):
        rt_counter = 0
        for tweet in self.tweets:
            if not self.graph.node_exists(tweet):
                self.create_node(tweet)
                self.create_nodes_mentions(tweet['mentioned_users'], tweet, rt_counter)
                rt_counter += 1

    def graph_of_rts(self):
        rt_counter = 0
        for tweet in self.tweets:
            if tweet['is_rt']:
                nodes = [
                    tweet,
                    get_user_info(tweet['who_was_rt'])
                ]
                self.create_nodes_rts(nodes)
                self.create_edge(nodes[0], nodes[1], rt_counter)
                rt_counter += 1

    def create_nodes_rts(self, nodes):
        for node in nodes:
            if not self.graph.node_exists(node):
                self.create_node(node)

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
            'followers': tweet['followers'],
            'verified': tweet['verified']
        }

        self.used_ids.append(node['Label'])
        self.graph.nodes.append(node)

    def create_nodes_mentions(self, mentions, who_mentioned, counter):
        if mentions != 'No Mentions':
            mentions_list = mentions.split(' ')
            for mention in mentions_list:
                if mention not in self.used_ids:
                    target_node = get_user_info(mention)
                else:
                    target_node = self.get_node(mention)
                if target_node is not None:
                    self.create_node(target_node)
                    self.create_edge(who_mentioned, target_node, counter)

    def get_node(self, target_node):
        for tweet in self.tweets:
            if target_node == tweet['Label']:
                return tweet


class GephiData:

    def __init__(self):
        self.nodes = []
        self.edges = []

    def node_exists(self, tweet):
        for node in self.nodes:
            if tweet['Id'] == node['Id']:
                return True
            return False


# Aux scraper method to get a specific user info
def get_user_info(username):

    try:
        user = sntwitter.TwitterUserScraper(username).entity
    except KeyError:
        print(f"User {username} suspended or not exist")
        user = None

    if user is not None:
        user_info = {
            'Id': user.id,
            'Label': user.username,
            'link': f'https://twitter.com/{user.username}',
            'verified': user.verified,
            'followers': user.followersCount
        }

        return user_info
    else:
        return None

