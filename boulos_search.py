"""
Scrape tweets that contains the keyword
'boulos', from november 15 to november 28,
1500 tweets per day.

@author: Bárbara Boechat
@date: 22/02/2021
"""
import json
from query_handler import *

get_tweets = Scraper()

dates = [('2020-11-15', '2020-11-16'), ('2020-11-16', '2020-11-17'),
         ('2020-11-17', '2020-11-18'), ('2020-11-18', '2020-11-19'),
         ('2020-11-19', '2020-11-20'), ('2020-11-20', '2020-11-21'),
         ('2020-11-21', '2020-11-22'), ('2020-11-22', '2020-11-23'),
         ('2020-11-23', '2020-11-24'), ('2020-11-24', '2020-11-25'),
         ('2020-11-25', '2020-11-26'), ('2020-11-26', '2020-11-27'),
         ('2020-11-27', '2020-11-28'), ('2020-11-28', '2020-11-29')]

json_array = []
for i in range(0, len(dates)):
    params = {
        'since_date': dates[i][0],
        'until_date': dates[i][1],
        'keyword': 'boulos',
        'max_tweets': 1500
    }
    print('Coletando: ', dates[i][0])
    json_array = get_tweets.cli_scrape_tweets_by_content(**params)

    jsonFile = open(f"boulos/coleta/{dates[i][0]}.json", "w+")
    jsonString = json.dumps(json_array)
    jsonFile.write(jsonString)
    jsonFile.close()

print('All done, have fun!')
