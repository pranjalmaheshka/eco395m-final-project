from database import engine 
from collections import Counter
from collections import defaultdict
from get_token import red_tokens
from get_token import twitter_tokens
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

article = [x for x in red_df['comment']]

entities_by_reddit = []
for doc in nlp.pipe(article):
    people = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.append(ent)
        if len(people) == 0:
            continue
    entities_by_reddit.append(people)


red_df['people'] = pd.Series(entities_by_reddit)
red_df['people'] = red_df['people'].astype(str)
print(len(red_df['people']), red_df)


# with engine.connect() as connection:
#   red_df.to_sql('temp_red_comm_entity', con=connection, if_exists='replace',index=False)


# reddit_comment_sql = """
#     UPDATE reddit_comments AS f
#     SET people = t.people
#     FROM temp_red_comm_entity AS t
#     WHERE f.reddit_post_id = t.reddit_post_id
# """

# with engine.begin() as conn:     # TRANSACTION
#     conn.execute(reddit_comment_sql)

'''Entity recognition for Tweets''' 
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

article = [x for x in tweet_df['tweet']]

entities_by_twitter = []
for doc in nlp.pipe(article):
    people = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.append(ent)
        if len(people) == 0:
            continue
    entities_by_twitter.append(people)


tweet_df['people'] = pd.Series(entities_by_twitter)
tweet_df['people'] = tweet_df['people'].astype(str)
print(len(tweet_df['people']), tweet_df)


# with engine.connect() as connection:
#   tweet_df.to_sql('temp_red_comm_entity', con=connection, if_exists='replace',index=False)


# twitter_comment_sql = """
#     UPDATE twitter_comments AS f
#     SET people = t.people
#     FROM temp_red_comm_entity AS t
#     WHERE f.reddit_post_id = t.reddit_post_id
# """

# with engine.begin() as conn:     # TRANSACTION
#     conn.execute(twitter_comment_sql)

######REDDIT
'''Analysis: top entities'''

reddit_person = []
for ent in red_tokens.ents:
    if ent.label_ == 'PERSON':
        reddit_person.append(ent.text)
        
reddit_person_counts = Counter(reddit_person).most_common(20)
red_df_person = pd.DataFrame(reddit_person_counts, columns =['text', 'count'])

print('Length of red_df_person', len(red_df_person), red_df_person)

'''Analysis: top nationalities, religious, and political groups'''
reddit_norp = []
for ent in red_tokens.ents:
    if ent.label_ == 'NORP':
        reddit_norp.append(ent.text)
        
reddit_norp_counts = Counter(reddit_norp).most_common(20)
red_df_norp = pd.DataFrame(reddit_norp_counts, columns =['text', 'count'])

print('Length of red_df_norp', len(red_df_norp), red_df_norp)


######TWITTER
'''Analysis: top entities'''

twitter_person = []
for ent in twitter_tokens.ents:
    if ent.label_ == 'PERSON':
        twitter_person.append(ent.text)
        
twitter_person_counts = Counter(twitter_person).most_common(20)
twitter_df_person = pd.DataFrame(twitter_person_counts, columns =['text', 'count'])

print('Length of twitter_person_counts', len(twitter_df_person), twitter_df_person)

'''Analysis: top nationalities, religious, and political groups'''
twitter_norp = []
for ent in twitter_tokens.ents:
    if ent.label_ == 'NORP':
        twitter_norp.append(ent.text)
        
twitter_norp_counts = Counter(twitter_norp).most_common(20)
twitter_df_norp = pd.DataFrame(twitter_norp_counts, columns =['text', 'count'])

print('Length of twitter_df_norp', len(twitter_df_norp), twitter_df_norp)

