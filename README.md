# py-twscraper

This project have the objective of retrieve data from twitter by using [Snsrape](https://github.com/JustAnotherArchivist/snscrape)
to do it, check they're documentation for more.

To get all the requirements of this repo install `Python>3` and run:

    pip install -r requirements.txt

This repo still is a work in progress and so far we've got a `main` script that
retrieve `1500` tweets and generates two graphs to be used in Gephi: 
- Mentions Graph
- Reteweets Graph

and generates a file for each graph with all the tweets contents to use in Iramuteq.

 