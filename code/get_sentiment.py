from database import engine
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download(["vader_lexicon"])
sia = SentimentIntensityAnalyzer()

import time
start = time.time()

def get_site_sentiment(site):
    if site == "Reddit":
        """Querying reddit comments from SQL"""
        query = """
        select * from reddit_comments rc limit 500 
        """
        likes = "upvotes"
        text = "comment"
        rtitle = "Reddit Score"
    elif site == "Twitter":
        """Querying Twitter comments from SQL"""
        query = """
        select * from twitter_comments tc limit 500
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
        comments["scaled_score"] = (comments["score_compound"] + 1)/2

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
            
        if site=="Reddit":
        print(comments)
        with engine.connect() as connection:
            comments.to_sql('temp_red_comm_sentiment', con=connection, if_exists='replace',index=False)

        reddit_sentiment_sql = """
            UPDATE reddit_comments AS f
            SET score_neg = t.score_neg, score_pos = t.score_pos, score_compound = t.score_compound, score = t.score
            FROM temp_red_comm_sentiment AS t
            WHERE f.reddit_post_id = t.reddit_post_id
            """
        with engine.begin() as conn:     # TRANSACTION
                conn.execute(reddit_sentiment_sql)

        if site=="Twitter":
            print(comments)
        with engine.connect() as connection:
                comments.to_sql('temp_twit_comm_sentiment', con=connection, if_exists='replace',index=False)

        twitter_sentiment_sql = """
            UPDATE twitter_comments AS f
            SET score_neg = t.score_neg, score_pos = t.score_pos, score_compound = t.score_compound, score = t.score
            FROM temp_twit_comm_sentiment AS t
            WHERE f.reddit_post_id = t.reddit_post_id
            """
        with engine.begin() as conn:     # TRANSACTION
                conn.execute(twitter_sentiment_sql)

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

    # Site level comparison 
    post_sentiment = comments.groupby(["reddit_post_id"])["scaled_score"].mean().reset_index()
    post_sentiment.columns =["Post ID", rtitle]

    return site_results, post_sentiment 

def get_sentiment():
    reddit_results, reddit_post_results = get_site_sentiment("Reddit")
    twitter_results, twitter_post_results = get_site_sentiment("Twitter")
    
    post_comparison = reddit_post_results.merge(twitter_post_results, on='Post ID', how='left')
    post_comparison["Diff"] = post_comparison["Twitter Score"] - post_comparison["Reddit Score"]
    # with engine.connect() as connection:
        #post_comparison.to_sql('post_comparison', con=connection, if_exists='replace',index=False)

    
    ################################################################################
    ## Ignore this part for now 
    test_neg = (post_comparison["Diff"] < 0).count()
    test_pos = (post_comparison["Diff"] > 0).count()

    print(test_neg)
    print(test_pos)

    diff_neg = post_comparison["Diff"][(post_comparison['Diff']>0)].mean(numeric_only=True,skipna=True)
    diff_pos = post_comparison[(post_comparison["Diff"]<0)].mean(numeric_only=True,skipna=True)
    diff_data = [["Reddit Positive", diff_neg], ["Twitter Positive", diff_pos]]
    diff_df = pd.DataFrame(diff_data, columns=["Mean Diff","Value"])
    
    #print("Mean difference in scores when Reddit is more positive is " + str(diff_neg))
    #print("Mean difference in scores when Twitter is more positive is " + str(diff_pos))
    ###############################################################################

    # send shit to database reddit_results twitter_results + new table for post_comparison
    return 

if __name__ == "__main__":
    get_sentiment()

ttime =  time.time() - start
print("Runtime is " + str(ttime))

#comments.to_csv("reddit_comments_pranjal.csv")
