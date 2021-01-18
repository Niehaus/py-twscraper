import csv
import snscrape.modules.twitter as sntwitter


class Scraper:

    @staticmethod
    def scrape_hashtag_tweets(filename, since_date, until_date, keyword, max_tweets):

        # Open/create a file to append data to
        filepath = 'scraped_tweets_csv/' + filename
        csv_file = open(filepath, 'a', newline='', encoding='utf8')

        # Use csv writer
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['username', 'content', 'mentionedUsers'])

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
                keyword + f' since:{since_date} '
                          f'until:{until_date} '
                          f'-filter:links '
                         ).get_items()):
            mentions = []
            if tweet.mentionedUsers is not None:
                for mentionedUser in tweet.mentionedUsers:
                    mentions.append(mentionedUser.username)

            row_tweet = {
                'username': tweet.user.username,
                'content': tweet.renderedContent,
                'mentionedUsers': ' '.join(mentions)
            }

            if i > max_tweets:
                break
            print(tweet)
            csv_writer.writerow([row_tweet['username'],
                                 row_tweet['content'],
                                 row_tweet['mentionedUsers']
                                 ])
        csv_file.close()
        print(f'Tweets scraped by hashtag, check out scraped_tweets_csv/{filename}.csv')

    @staticmethod
    def arestas_by_mentions():
        ...
