import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

reddit_comments = pd.read_csv("reddit_comment_results.csv")

reddit_comments['score_neg'] = 0
reddit_comments['score_neu'] = 0
reddit_comments['score_pos'] = 0
reddit_comments['score_compound'] = 0
reddit_comments['score'] = 0
# Vader: 1 is neg, 2 is neu, 3 is pos 

for ind in reddit_comments.index:
    score = sia.polarity_scores(reddit_comments.loc[ind][2])
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
