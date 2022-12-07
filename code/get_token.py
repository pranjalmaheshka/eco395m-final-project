from database import engine 
from collections import Counter
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 100000000

'''Cleaning Reddit data'''
reddit_comments = """
select 
    reddit_post_id, 
    comment
from 
    reddit_comments rc
group by 
    rc.reddit_post_id, rc.comment 
"""

red_df = pd.read_sql_query(reddit_comments, engine)

red_df['comment'] = red_df['comment'].astype(str)

red_df['tokenized'] = red_df['comment'].apply(lambda x: nlp(x))

red_df['lemmatized'] = red_df['tokenized'].apply(lambda x: [y.lemma_ for y in nlp(x)])

red_tokens = nlp(''.join(str(red_df.lemmatized.tolist())))

red_items = [x.text for x in red_tokens.ents]

red = Counter(red_items).most_common(50)

red_tokens_df = pd.DataFrame.from_records(red, columns=['Token','Count'])

print('Length of Reddit tokens', len(red_tokens_df), red_tokens_df) 


'''Cleaning Twitter data'''
twitter_comments = """
select 
    reddit_post_id, 
    tweet
from 
    twitter_comments tc
group by 
    tc.reddit_post_id, tc.tweet limit 50
"""

tweet_df = pd.read_sql_query(twitter_comments, engine)

tweet_df['tweet'] = tweet_df['tweet'].astype(str)

tweet_df['tokenized'] = tweet_df['tweet'].apply(lambda x: nlp(x))

tweet_df['lemmatized'] = tweet_df['tokenized'].apply(lambda x: [y.lemma_ for y in nlp(x)])

twitter_tokens = nlp(''.join(str(tweet_df.lemmatized.tolist())))

twitter_items = [x.text for x in twitter_tokens.ents]

twit = Counter(twitter_items).most_common(50)

twit_tokens_df = pd.DataFrame.from_records(twit, columns=['Token','Count'])

print('Length of Twitter tokens', len(twit_tokens_df), twit_tokens_df) 
