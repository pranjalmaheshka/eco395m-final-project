import os
import pandas as pd
from dotenv import load_dotenv
from database import engine
import snscrape.modules.twitter as sntwitter


load_dotenv()


def twitter_scraper(sql_data):
    df = sql_data
    for index, row in df.iterrows():
        data = []
        id_list = []
        string = row["title"][:250].replace("“","").replace("”","")
        print(string)
        for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(string, top=True).get_items()
        ):
            if i > 4:
                break
            if tweet.id in id_list:
                continue
            id_list.append(tweet.id)
            data.append(
                [
                    row["reddit_post_id"],
                    row["title"],
                    row["url"],
                    tweet.date,
                    tweet.user.username,
                    tweet.user.description,
                    tweet.user.verified,
                    tweet.content,
                    tweet.url,
                    tweet.id,
                    tweet.replyCount,
                    tweet.retweetCount,
                    tweet.likeCount,
                ]
            )
        print("headline search done")

        for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(row["url"], top=True).get_items()
        ):
            if i > 4:
                break
            if tweet.id in id_list:
                continue
            id_list.append(tweet.id)
            data.append(
                [
                    row["reddit_post_id"],
                    row["title"],
                    row["url"],
                    tweet.date,
                    tweet.user.username,
                    tweet.user.description,
                    tweet.user.verified,
                    tweet.content,
                    tweet.url,
                    tweet.id,
                    tweet.replyCount,
                    tweet.retweetCount,
                    tweet.likeCount,
                ]
            )
        print("url search done")

        for id in id_list:
            id_list2 = []
            mode = sntwitter.TwitterTweetScraperMode
            sncraper_reply = sntwitter.TwitterTweetScraper(tweetId=id, mode=mode.SCROLL)
            replies = sncraper_reply.get_items()
            for tweet in replies:
                if tweet.id in id_list or tweet.id in id_list2:
                    continue
                id_list2.append(tweet.id)
                data.append(
                    [
                        row["reddit_post_id"],
                        row["title"],
                        row["url"],
                        tweet.date,
                        tweet.user.username,
                        tweet.user.description,
                        tweet.user.verified,
                        tweet.content,
                        tweet.url,
                        tweet.id,
                        tweet.replyCount,
                        tweet.retweetCount,
                        tweet.likeCount,
                    ]
                )
        print("replies search done")

        headers = [
            "reddit_post_id",
            "title",
            "url",
            "date_posted",
            "twitter_user",
            "user_desc",
            "verified",
            "tweet",
            "tweet_url",
            "tweet_id",
            "reply_count",
            "retweet_count",
            "likes",
        ]
        output = pd.DataFrame(data, columns=headers)
        output.to_sql("twitter_comments", con=engine, if_exists="append", index=False)
    print("completed")


def nlp_columns():
    query_template = """
    ALTER TABLE twitter_comments
    add people varchar,
    add organization varchar,
    add score_neg numeric,
    add score_neu numeric,
    add score_pos numeric,
    add score_compound numeric,
    add score numeric;
    """

    with engine.connect() as connection:
        connection.exec_driver_sql(query_template)


if __name__ == "__main__":
    myquery = """
	SELECT reddit_post_id, title, url FROM reddit_posts OFFSET 45;
	"""
    df = pd.read_sql_query(myquery, engine)
    twitter_scraper(df)
    #nlp_columns()
