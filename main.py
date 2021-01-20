"""
Coleta de tweets de março a dezembro
para duas hashtags:
['cloroquina', 'hidroxicloroquina']

@author: Bárbara Boechat
@date: 18/01/2021
"""
from query_handler import Scraper
from gephi_usage import Gephi
from pprint import pprint
from utils import csv_handler, get_key_list

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

keywords = ['cloroquina', 'hidroxicloroquina']

# for keyword in keywords:
#     for i in range(0, len(filenames)):
#         params = {
#             'filename': 'cloroquina_' + filenames[i],
#             'since_date': dates[i][0],
#             'until_date': dates[i][1],
#             'keyword': keywords,
#             'max_tweets': 1500
#         }
#         print(params)
#         twitter_scraper.scrape_hashtag_tweets(**params)
#     print('\n')

params = {
    'since_date': dates[1][0],
    'until_date': dates[1][1],
    'keyword': keywords[0],
    'max_tweets': 150
}

# filename = 'cloroquina_' + filenames[1]
# headers = ['Id', 'Label', 'mentioned_users']
# csv_handler('result_test', content, headers)

scraped_tweets = twitter_scraper.cli_scrape_tweets_by_content(**params)
gephi_content = Gephi(scraped_tweets)
# gephi_content.graph_of_mentions()
gephi_content.graph_of_rts()

# Get headers for Gephi csv files
nodes_headers = get_key_list(
                gephi_content.graph.nodes[-1])
edges_headers = get_key_list(
                gephi_content.graph.edges[-1])

print('writing nodes')
# Write node files for retweets
csv_handler(
    'nodes_rt_abril',
    gephi_content.graph.nodes,
    nodes_headers
)
print('writing edges')
# Write edges files for retweets
csv_handler(
    'edges_rt_abril',
    gephi_content.graph.edges,
    edges_headers
)

