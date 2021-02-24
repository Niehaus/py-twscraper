"""
Create graph to be used at Gephi with scraped tweets
that contains the keyword 'boulos', from november
15 to november 28, 1500 tweets per day.

@author: Bárbara Boechat
@date: 22/02/2021
"""
import json
import sys
from time import sleep

from gephi_usage import *
from utils import write_gephi_files

if __name__ == '__main__':
    file = sys.argv[1]
    with open(f'boulos/coleta/{file}') as json_file:
        tweets = json.load(json_file)

    # # # Create graph of mentions
    # gephi = Gephi(tweets)
    # gephi.graph_of_mentions()
    #
    # date = ''.join(file.split(".json"))
    # filename = f'boulos/gephi_files/mentions/mentions_{date}'
    # write_gephi_files(gephi.graph, filename)
    #
    # sleep(180)

    # Create graph of retweets
    gephi = Gephi(tweets)
    gephi.graph_of_rts()

    if gephi.graph.nodes:
        date = ''.join(file.split(".json"))
        filename = f'boulos/gephi_files/rts/rts_{date}'
        write_gephi_files(gephi.graph, filename)
    else:
        print('0 tweets were quoted ):')

