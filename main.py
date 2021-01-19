"""
Coleta de tweets de março a dezembro
para duas hashtags:
['cloroquina', 'hidroxicloroquina']

@author: Bárbara Boechat
@date: 18/01/2021
"""
from query_handler import Scraper
from utils import csv_handler

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
    'filename': 'cloroquina_' + filenames[1],
    'since_date': dates[1][0],
    'until_date': dates[1][1],
    'keyword': keywords[0],
    'max_tweets': 15
}

content = twitter_scraper.scrape_tweets_by_content(**params)
# twitter_scraper.get_user_info('leugolas')

row = ['Id', 'Label', 'mentioned_users']
csv_handler('result_test', content, row)
