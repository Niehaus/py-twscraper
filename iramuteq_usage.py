# -*- coding: utf-8 -*-
import re


class Iramuteq:
    def __init__(self, nodes, scraped_tweets, variables):
        self.nodes = nodes
        self.tweets = self.get_used_tweets(scraped_tweets)
        self.variables = variables

    def get_used_tweets(self, scraped_tweets):
        tweets_content = []
        for node in self.nodes:
            for tweet in scraped_tweets:
                if node['Id'] == tweet['Id']:
                    tweets_content.append(tweet['content'])

        return tweets_content

    def create_file(self, filename):
        iramuteq_file = open(
            f'./iramuteq_files/{filename}.txt',
            "w", encoding="utf-8")
        inicia_comando = "*" * 4

        for i in range(len(self.tweets)):
            p = re.compile('\w+')  # retira todos os simbolos não alfa-numericos
            description = p.findall(self.tweets[i])
            description = ' '.join(description)

            line = f'{inicia_comando} '
            for variable in self.variables:
                line += f'*{variable} '
            line += f'\n{description}\n\n'

            iramuteq_file.write(line)
        print(f'Iramuteq file written in iramuteq_files/{filename}')
