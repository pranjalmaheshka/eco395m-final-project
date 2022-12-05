from database import engine
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

import matplotlib
import time
start = time.time()

#reddit_comments = pd.read_csv("reddit_comment_results.csv")

"""Querying reddit posts from SQL"""
posts = """
select * from reddit_posts rp limit 100
"""
posts_df = pd.read_sql_query(posts, engine)
#print(posts_df)

"""Querying reddit comments from SQL"""
comments = """
select * from reddit_comments rc limit 100
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

upvotes_series = reddit_comments.groupby(['score'])['upvotes'].sum()
sentiments_df = reddit_comments.groupby(['score'])['score'].count()
sentiments = ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]
print(upvotes_series)
print(sentiments_df)
#print(type(sentiments_df))

votes_by_sentiment = upvotes_series/sentiments_df
results = pd.concat([sentiments, upvotes_series, sentiments_df,votes_by_sentiment], axis=1)
results.columns =["Sentiment", "Sentiment Count", "Total Upvotes", "Avg Upvotes"]
print(results)
print(results.hist)

end = time.time()
ttime = end - start
print("Runtime is " + str(ttime))

reddit_comments.to_csv("reddit_comments_pranjal.csv")
