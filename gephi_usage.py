import snscrape.modules.twitter as sntwitter


class Gephi:

    def __init__(self, scraped_tweets):
        self.tweets = scraped_tweets
        self.used_ids = []
        self.suspended_users_id = [-1]
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
                nodes = [
                    tweet,
                    self.get_user_info(tweet['who_was_rt'])
                ]
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

    def get_node(self, username):
        for tweet in self.graph.nodes:
            if username == tweet['Label']:
                return tweet

    # Aux scraper method to get a specific user info
    def get_user_info(self, username):
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
            user_id = self.suspended_users_id[-1] + 1
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

