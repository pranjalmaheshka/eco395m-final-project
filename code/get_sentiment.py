from database import engine
import pandas as pd
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download(["vader_lexicon"])
sia = SentimentIntensityAnalyzer()

def get_site_sentiment(site):
    """ This pulls scraped data from Reddit or Twitter and then uses VADER to analyze sentiments. The outputs are used to compare both sites and the sentiment analysis is directed uploaded to a SQL Database on GCP."""
    if site == "Reddit":
        """Querying reddit comments from SQL"""
        query = """
        select * from reddit_comments rc
        """
        likes = "upvotes"
        text = "comment"
        rtitle = "Reddit Score"
    elif site == "Twitter":
        """Querying Twitter comments from SQL"""
        query = """
        select * from twitter_comments tc 
        """
        likes = "likes"
        text = "tweet"
        rtitle = "Twitter Score"

    comments = pd.read_sql_query(query, engine)

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
            comments.at[ind,'score'] = 3
        comments = comments.astype({"score_neg": float, "score_neu": float, "score_pos": float, "score_compound": float, "score":float})

    # Site level analysis
    sentiments = pd.Series(["","Very Negative", "Negative", "Neutral", "Positive", "Very Positive"])
    sentiments_count = comments.groupby(['score'])['score'].count()
    sentiments_pct = sentiments_count/len(sentiments_count)
    upvotes_count = comments.groupby(['score'])[likes].sum()
    upvotes_pct = upvotes_count*100/sum(upvotes_count)
    votes_by_sentiment = upvotes_count/sentiments_count

    site_results = pd.concat([sentiments, sentiments_count, sentiments_pct, upvotes_pct, votes_by_sentiment], axis=1)
    site_results.columns =["Sentiment", "Sentiment Count", "Sentiment Pct", "Upvotes Pct", "Upvotes Avg"]
    site_results = site_results.iloc[1: , :]
    site_results.index.name=None
    site_results = site_results.astype({"Upvotes Avg": int})
    test1 = site_results[["Sentiment Count", "Sentiment Pct", "Upvotes Pct"]]
    
    if site=="Reddit":
        site_results.to_sql('reddit_site-results', con=engine, if_exists='replace',index=False)
    
    if site=="Twitter":
        site_results.to_sql('twitter_site-results', con=engine, if_exists='replace',index=False)

    # Site level comparison
    post_sentiment = comments.groupby(["reddit_post_id"])["score_compound"].mean().reset_index()
    post_sentiment.columns =["Post ID", rtitle]

    if site=="Reddit":
        comments.to_sql('temp_red_comm_sentiment', con=engine, if_exists='replace',index=False)

        reddit_sentiment_sql = """
            UPDATE reddit_comments AS f
            SET score_neg = t.score_neg, score_neu = t.score_neu, score_pos = t.score_pos, score_compound = t.score_compound, score = t.score
            FROM temp_red_comm_sentiment AS t
            WHERE t.id = f.id
            """
        with engine.connect() as connection:
            connection.exec_driver_sql(reddit_sentiment_sql)

    if site=="Twitter":
        comments.to_sql('temp_twit_comm_sentiment', con=engine, if_exists='replace',index=False)

        twitter_sentiment_sql = """
            UPDATE twitter_comments AS f
            SET score_neg = t.score_neg, score_neu = t.score_neu, score_pos = t.score_pos, score_compound = t.score_compound, score = t.score
            FROM temp_twit_comm_sentiment AS t
            WHERE t.id = f.id
            """
        with engine.connect() as connection:
            connection.exec_driver_sql(twitter_sentiment_sql)

    return site_results, post_sentiment

def get_sentiment():
    """Calls function to analyze Reddit and Twitter and then compares outputs."""
    reddit_results, reddit_post_results = get_site_sentiment("Reddit")
    twitter_results, twitter_post_results = get_site_sentiment("Twitter")

    post_comparison = reddit_post_results.merge(twitter_post_results, on='Post ID', how='left')    
    post_comparison["Diff"] = post_comparison["Twitter Score"] - post_comparison["Reddit Score"]
    post_comparison['Same'] = np.where(abs(post_comparison['Diff'])<= 0.2, True, False)
    
    post_comparison.to_sql('post_comparison', con=engine, if_exists='replace',index=False)

    return

if __name__ == "__main__":
    get_sentiment()
