from database import engine 
from collections import Counter
from collections import defaultdict
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 5000000

'''Entity recognition for Reddit comments'''
reddit_comments = """
select 
    reddit_post_id, 
    comment
from 
    reddit_comments rc
group by 
    rc.reddit_post_id, rc.comment limit 50 
"""

red_df = pd.read_sql_query(reddit_comments, engine)

red_df['comment'] = red_df['comment'].astype(str)

red_tokens = nlp(''.join(str(red_df.comment.tolist())))

red_items = [x.text for x in red_tokens.ents]

red = Counter(red_items).most_common(50)

#df = pd.DataFrame.from_records(c.most_common(), columns=['Token','Count'])

print('Length of Reddit tokens', len(red), red) 


'''Entity recognition for Twitter comments'''
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

twitter_tokens = nlp(''.join(str(tweet_df.tweet.tolist())))

twitter_items = [x.text for x in twitter_tokens.ents]

twit = Counter(twitter_items).most_common(50)

#df = pd.DataFrame.from_records(c.most_common(), columns=['Token','Count'])

print('Length of Twitter tokens', len(twit), twit) 

