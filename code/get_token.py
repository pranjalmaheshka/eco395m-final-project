from database import engine
from collections import Counter
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 100000000

reddit_comments = """
select
    id,
    reddit_post_id,
    comment
from
    reddit_comments rc
group by
    rc.reddit_post_id, rc.comment, rc.id
"""


def get_reddit_tokens():
    """Cleaning Reddit data"""
    red_df = pd.read_sql_query(reddit_comments, engine)

    red_df["comment"] = red_df["comment"].astype(str)

    red_df["tokenized"] = red_df["comment"].apply(lambda x: nlp(x))

    red_df["tokenized"] = red_df["tokenized"].astype(str)

    red_tokens = nlp("".join(str(red_df.tokenized.tolist())))

    red_items = [x.text for x in red_tokens.ents]

    red = Counter(red_items).most_common(50)

    red_tokens_df = pd.DataFrame.from_records(red, columns=["Token", "Count"])


twitter_comments = """
select
    id,
    reddit_post_id,
    tweet
from
    twitter_comments tc
group by
    tc.reddit_post_id, tc.tweet, tc.id
"""


def get_twitter_tokens():
    """Cleaning Twitter data"""
    tweet_df = pd.read_sql_query(twitter_comments, engine)

    tweet_df["tweet"] = tweet_df["tweet"].astype(str)

    tweet_df["tokenized"] = tweet_df["tweet"].apply(lambda x: nlp(x))

    tweet_df["tokenized"] = red_df["tokenized"].astype(str)

    twitter_tokens = nlp("".join(str(tweet_df.tokenized.tolist())))

    twitter_items = [x.text for x in twitter_tokens.ents]

    twit = Counter(twitter_items).most_common(50)

    twit_tokens_df = pd.DataFrame.from_records(twit, columns=["Token", "Count"])


twitter_desc = """
select
    id, reddit_post_id,
    user_desc
from
    twitter_comments tc
group by
    tc.reddit_post_id, tc.user_desc, tc.id
"""


def get_twituser_tokens():
    """Cleaning Twitter descriptions"""
    desc_df = pd.read_sql_query(twitter_desc, engine)

    desc_df["user_desc"] = desc_df["user_desc"].astype(str)

    desc_df["tokenized"] = desc_df["user_desc"].apply(lambda x: nlp(x))

    desc_df["tokenized"] = red_df["tokenized"].astype(str)

    desc_tokens = nlp("".join(str(desc_df.tokenized.tolist())))

    twitter_desc_items = [x.text for x in desc_tokens.ents]

    desc = Counter(twitter_desc_items).most_common(50)

    desc_tokens_df = pd.DataFrame.from_records(desc, columns=["Token", "Count"])
