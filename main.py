"""
Scrape tweets that has in its contents
two words 'cloroquina', 'hidroxicloroquina'
from march to december of 2020.

@author: Bárbara Boechat
@date: 18/01/2021
"""
from query_handler import Scraper
from gephi_usage import Gephi
from iramuteq_usage import Iramuteq
from pprint import pprint
from utils import *
import snscrape.modules.twitter as sntwitter
twitter_scraper = Scraper()

filenames = ['marco', 'abril', 'maio', 'junho', 'julho',
             'agosto', 'setembro', 'outubro', 'novembro',
             'dezembro']

dates = [('2020-03-01', '2020-03-31'),  # março
         ('2020-04-01', '2020-04-30'),  # abril
         ('2020-05-01', '2020-05-31'),  # maio
         ('2020-06-01', '2020-06-30'),  # junho
         ('2020-07-01', '2020-07-31'),  # julho
         ('2020-08-01', '2020-08-31'),  # agosto
         ('2020-09-01', '2020-09-30'),  # setembro
         ('2020-10-01', '2020-10-31'),  # outubro
         ('2020-11-01', '2020-11-30'),  # novembro
         ('2020-12-01', '2020-12-31')]  # dezembro

# keywords = ['cloroquina', 'hidroxicloroquina']
keywords = ['hidroxicloroquina']

for keyword in keywords:
    for i in range(1, len(filenames)):
        params = {
            'since_date': dates[i][0],
            'until_date': dates[i][1],
            'keyword': keyword,
            'max_tweets': 750
        }
        pprint(params)

        # Scrape all needed tweets
        scraped_tweets = twitter_scraper.cli_scrape_tweets_by_content(**params)

        # Create the graph of mentions
        gephi = Gephi(scraped_tweets)
        gephi.graph_of_mentions()

        filename = f'gephi_files/mentions/{keyword}_mentions_{filenames[i]}'
        write_gephi_files(gephi.graph, filename)

        # Create iramuteq file for mentions
        variables = ['tweet', 'mentions']
        iramuteq_mentions = Iramuteq(
            gephi.graph.nodes,
            scraped_tweets,
            variables
        )
        filename = f'{keyword}_mentions_{filenames[i]}'
        iramuteq_mentions.create_file(filename)

        # Create the graph of retweets
        # gephi = Gephi(scraped_tweets)
        # gephi.graph_of_rts()
        #
        # filename = f'gephi_files/rts/{keyword}_rts_{filenames[i]}'
        # write_gephi_files(gephi.graph, filename)
        #
        # # Create iramuteq file for retweets
        # variables = ['tweet', 'rts']
        # iramuteq_mentions = Iramuteq(
        #     gephi.graph.nodes,
        #     scraped_tweets,
        #     variables
        # )
        # filename = f'{keyword}_rts_{filenames[i]}'
        # iramuteq_mentions.create_file(filename)
        print('Next up!\n')
print('All clear, have fun! :D')
