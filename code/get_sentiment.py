from database import engine
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

import time
start = time.time()

"""Querying reddit posts from SQL"""
posts = """
select * from reddit_posts rp 
"""
posts_df = pd.read_sql_query(posts, engine)

"""Querying reddit comments from SQL"""
comments = """
select * from reddit_comments rc
"""
reddit_comments = pd.read_sql_query(comments, engine)

# Vader: 1 is neg, 2 is neu, 3 is pos 
for ind in reddit_comments.index:
    score = sia.polarity_scores(reddit_comments.loc[ind]["comment"])
    reddit_comments.at[ind,'score_neg'] = score["neg"]
    reddit_comments.at[ind,'score_neu'] = score["neu"]
    reddit_comments.at[ind,'score_pos'] = score["pos"]
    reddit_comments.at[ind,'score_compound'] = score["compound"]

    # Creating new scoring system: 1 = very neg, 2 = neg, 3 = neu, 4 = pos, 5 = very pos 
    if score["neg"] >= 0.5:
        reddit_comments.at[ind,'score'] = 1
    elif score["pos"] >= 0.5:
        reddit_comments.at[ind,'score'] = 5
    elif abs(score["neg"]-score["pos"]) > 0.20:      
        if score["neg"] > score["pos"]:
            reddit_comments.at[ind,'score'] = 1
        else:
            reddit_comments.at[ind,'score'] = 5
    elif abs(score["neg"]-score["pos"]) <= 0.10:
            reddit_comments.at[ind,'score'] = 3
    elif abs(score["neg"]-score["pos"]) <= 0.20:
            if score["neg"] > score["pos"]:
                reddit_comments.at[ind,'score'] = 2
            else:
                reddit_comments.at[ind,'score'] = 4
    else:
        reddit_comments.at[ind,'score'] = 100

sentiments = pd.Series(["","Very Negative", "Negative", "Neutral", "Positive", "Very Positive"])
sentiments_df = reddit_comments.groupby(['score'])['score'].count()
upvotes_series = reddit_comments.groupby(['score'])['upvotes'].sum()
votes_by_sentiment = upvotes_series/sentiments_df

results = pd.concat([sentiments, upvotes_series, sentiments_df,votes_by_sentiment], axis=1)
results.columns =["Sentiment", "Sentiment Count", "Total Upvotes", "Avg Upvotes"]
results = results.iloc[1: , :]
results.index.name=None
results = results.astype({"Avg Upvotes": int})
print(results)

ttime =  time.time() - start
print("Runtime is " + str(ttime))

reddit_comments.to_csv("reddit_comments_pranjal.csv")
