import snscrape.modules.twitter as sntwitter
from time import sleep
from utils import write_rts


class Gephi:

    def __init__(self, scraped_tweets):
        self.tweets = scraped_tweets
        self.used_ids = []
        self.retweets_counter = []
        self.suspended_users_id = [-1]
        self.multi = 1
        self.graph = GephiData()

    def graph_of_mentions(self):
        for tweet in self.tweets:
            if tweet['Label'] not in self.used_ids:
                self.create_node(tweet)
                self.create_nodes_mentions(tweet['mentioned_users'], tweet)

    def test_func(self):
        print(self.get_user_info('diegoescosteguy'))

    def graph_of_rts(self):
        for tweet in self.tweets:
            if tweet['is_rt']:
                # self.retweets_counter.append(tweet['rt_id'])
                nodes = [
                    tweet,
                    self.get_user_info(tweet['who_was_rt'])
                ]
                # write_rts(tweet)
                try:
                    self.create_nodes_rts(nodes)
                    self.create_edge(nodes[0], nodes[1])
                except Exception:
                    pass

    def create_nodes_rts(self, nodes):
        for node in nodes:
            if node['Label'] not in self.used_ids:
                self.create_node(node)

    def create_edge(self, source, target):
        try:
            counter = self.graph.edges[-1]['Label'] + 1
        except IndexError:
            counter = 0
        edge = {
            'Source': source['Id'],
            'Target': target['Id'],
            'Type': 'Directed',
            'Label': counter,
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

    def create_nodes_mentions(self, mentions, who_mentioned):
        if mentions != 'No Mentions':
            mentions_list = mentions.split(' ')
            for mention in mentions_list:
                try:
                    if mention not in self.used_ids:
                        target_node = self.get_user_info(mention)
                        self.create_node(target_node)
                    else:
                        target_node = self.get_node(mention)
                    self.create_edge(who_mentioned, target_node)
                except Exception:
                    pass

    def get_retweet_ranking(self):
        rt_ranking = []
        for rt_id in self.retweets_counter:
            count = self.retweets_counter.count(rt_id)
            my_tuple = (rt_id, count)
            rt_ranking.append(my_tuple)
        rt_ranking = sorted(rt_ranking, key=lambda x: x[1], reverse=True)

    def get_node(self, username):
        for tweet in self.graph.nodes:
            if username == tweet['Label']:
                return tweet

    # Aux scraper method to get a specific user info
    def get_user_info(self, username):
        edges_count = len(self.graph.edges) > 0
        if edges_count and self.graph.edges[-1]['Label'] + 1 >= 800 * self.multi:
            print('muitos perfiss, perai', self.graph.edges[-1]['Label'] + 1)
            self.multi += 1
            sleep(180)
            print('beleza, bora')
        try:
            user = sntwitter.TwitterUserScraper(username).entity
            user_info = {
                'Id': user.id,
                'Label': user.username,
                'link': f'https://twitter.com/{user.username}',
                'verified': user.verified,
                'followers': user.followersCount
            }
            return user_info
        except Exception:
            user_id = abs(hash(username))
            self.suspended_users_id.append(user_id)
            user_info = {
                'Id': user_id,
                'Label': username,
                'link': f'https://twitter.com/{username}',
                'verified': False,
                'followers': -1
            }
            print(f"User {username} suspended or not exist \n",
                  f'Standard node for non-existent account created. '
                  f'Id: {user_id}')
            return user_info


class GephiData:

    def __init__(self):
        self.nodes = []
        self.edges = []

    def node_exists(self, tweet):
        for node in self.nodes:
            if tweet['Id'] == node['Id']:
                return True
            return False
