from database import engine
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

import time
start = time.time()

def get_sentiment(site):
    if site == "Reddit":
        """Querying reddit comments from SQL"""
        query = """
        select * from reddit_comments rc limit 50
        """
        likes = "upvotes"
        text = "comment"
    elif site == "Twitter":
        """Querying Twitter comments from SQL"""
        query = """
        select * from twitter_comments tc limit 1000
        """
        likes = "likes"
        text = "tweet"
    
    comments = pd.read_sql_query(query, engine)
    print(comments.columns)

    # Vader: 1 is neg, 2 is neu, 3 is pos 
    for ind in comments.index:
        score = sia.polarity_scores(comments.loc[ind][text])
        comments.at[ind,'score_neg'] = score["neg"]
        comments.at[ind,'score_neu'] = score["neu"]
        comments.at[ind,'score_pos'] = score["pos"]
        comments.at[ind,'score_compound'] = score["compound"]

        # Creating new scoring system: 1 = very neg, 2 = neg, 3 = neu, 4 = pos, 5 = very pos 
        if score["neg"] >= 0.5:
            comments.at[ind,'score'] = 1
        elif score["pos"] >= 0.5:
            comments.at[ind,'score'] = 5
        elif abs(score["neg"]-score["pos"]) > 0.20:      
            if score["neg"] > score["pos"]:
                comments.at[ind,'score'] = 1
            else:
                comments.at[ind,'score'] = 5
        elif abs(score["neg"]-score["pos"]) <= 0.10:
                comments.at[ind,'score'] = 3
        elif abs(score["neg"]-score["pos"]) <= 0.20:
                if score["neg"] > score["pos"]:
                    comments.at[ind,'score'] = 2
                else:
                    comments.at[ind,'score'] = 4
        else:
            comments.at[ind,'score'] = 100

    # Try testing code with removing comments that are less than 50 characters 
    sentiments = pd.Series(["","Very Negative", "Negative", "Neutral", "Positive", "Very Positive"])
    sentiments_df = comments.groupby(['score'])['score'].count()
    upvotes_series = comments.groupby(['score'])[likes].sum()
    votes_by_sentiment = upvotes_series/sentiments_df

    results = pd.concat([sentiments, upvotes_series, sentiments_df,votes_by_sentiment], axis=1)
    results.columns =["Sentiment", "Sentiment Count", "Total Upvotes", "Avg Upvotes"]
    results = results.iloc[1: , :]
    results.index.name=None
    results = results.astype({"Avg Upvotes": int})

    # Cross site - post by post analysis 
    post1 = comments.groupby(["reddit_post_id","score"])[likes].sum()
    post2 = comments.groupby(["reddit_post_id","score"])["score"].count()
    postresults= pd.concat([post1, post2], axis=1)

    post1.reset_index(name='Likes').to_string(index=False)
    post2.reset_index(name='Comment Count').to_string(index=False)

    #print(post1)
    #print(type(post1))
    
    postresults= pd.concat([post1, post2], axis=1)
    #print(postresults)
    postresults = postresults.iloc[1: , :]
    #print(postresults)
    print(type(postresults))
    print(postresults.columns)
    postresults = postresults.rename(columns={'reddit_post_id': 'PostID'})
    print(postresults)

    return results, postresults 

def sentiment_results():
    results1 = get_sentiment("Reddit")
    results2 = get_sentiment("Twitter")
    
    return 

if __name__ == "__main__":
    results, posts = get_sentiment("Reddit")
    print("Reddit results are")
    print(results)
    #results = get_sentiment("Twitter")
    #print("Twitter results are")
    #print(results)

ttime =  time.time() - start
print("Runtime is " + str(ttime))

#comments.to_csv("reddit_comments_pranjal.csv")
