import snscrape.modules.twitter as sntwitter


class Scraper:

    @staticmethod
    def scrape_tweets_by_content(filename, since_date, until_date, keyword, max_tweets):
        scraped_tweets = []
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
                'Id': tweet.id,
                'Label': tweet.user.username,
                'content': tweet.renderedContent,
                'mentioned_users': ' '.join(mentions)
            }
            scraped_tweets.append(row_tweet)
            if i > max_tweets:
                break

        return scraped_tweets

    @staticmethod
    def arestas_by_mentions():
        ...

    @staticmethod
    def get_user_info(username):
        user = sntwitter.TwitterUserScraper(username).entity
        user_info = {
            'id': user.id,
            'linkUrl': f'https://twitter.com/{user.username}',
            'username': user.username,
            'verified': user.verified,
            'followersCount': user.followersCount
        }

        return user_info
