from database import engine
from collections import Counter
from get_token import red_tokens
from get_token import red_df
from get_token import twitter_tokens
from get_token import tweet_df
from get_token import desc_tokens
from get_token import desc_df
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 5000000

def get_reddit_people():
    '''Entity recognition for people in Reddit comments'''
    reddit_person = []
    for ent in red_tokens.ents:
        if ent.label_ == 'PERSON':
            reddit_person.append(ent.text)
        if len(reddit_person) == 0:
                continue

    red_df['people'] = pd.Series(reddit_person)
    red_df['people'] = red_df['people'].astype(str)
print(len(red_df['people']), red_df)

def get_reddit_org():
    '''Entity recognition for organizations in Reddit comments'''
    reddit_org = []
    for ent in red_tokens.ents:
        if ent.label_ == 'ORG':
            reddit_org.append(ent.text)
        if len(reddit_org) == 0:
            continue

    red_df['organization'] = pd.Series(reddit_org)
    red_df['organization'] = red_df['organization'].astype(str)

def get_reddit_norp():
    '''Entity recognition for NORP in Reddit comments'''
    reddit_norp = []
    for ent in red_tokens.ents:
        if ent.label_ == 'NORP':
            reddit_norp.append(ent.text)
        if len(reddit_norp) == 0:
            continue

    red_df['NORP'] = pd.Series(reddit_norp)
    red_df['NORP'] = red_df['NORP'].astype(str)

def upload_reddit_entity():
    '''Upload entities in Reddit comments'''
    red_df.to_sql('temp_red_comm_entity', con=engine, if_exists='replace',index=False)

    reddit_comment_sql = """
        UPDATE reddit_comments AS f
        SET people = t.people, organization = t.organization, norp = t."NORP"
        FROM temp_red_comm_entity AS t
        WHERE f.id = t.id
    """
    
    with engine.begin() as conn:     # Transaction
        conn.exec_driver_sql(reddit_comment_sql)


def get_twitter_people():
    '''Entity recognition for people in Tweets'''
    twitter_person = []
    for ent in twitter_tokens.ents:
        if ent.label_ == 'PERSON':
            twitter_person.append(ent.text)
        if len(twitter_person) == 0:
            continue

    tweet_df['people'] = pd.Series(twitter_person)
    tweet_df['people'] = tweet_df['people'].astype(str)

def get_twitter_org():
    '''Entity recognition for organizations in Tweets'''
    twitter_org = []
    for ent in twitter_tokens.ents:
        if ent.label_ == 'ORG':
            twitter_org.append(ent.text)
        if len(twitter_org) == 0:
            continue

    tweet_df['organization'] = pd.Series(twitter_org)
    tweet_df['organization'] = tweet_df['organization'].astype(str)

def get_twitter_norp():
    '''Entity recognition for NORP in Tweets'''
    twitter_norp = []
    for ent in twitter_tokens.ents:
        if ent.label_ == 'NORP':
            twitter_norp.append(ent.text)
        if len(twitter_norp) == 0:
            continue

    tweet_df['NORP'] = pd.Series(twitter_norp)
    tweet_df['NORP'] = tweet_df['NORP'].astype(str)

def upload_twitter_entity():
    '''Upload entities in Tweets'''
    tweet_df.to_sql('temp_twit_comm_entity', con=engine, if_exists='replace',index=False)

    twitter_comment_sql = """
        UPDATE twitter_comments AS f
        SET people = t.people, organization = t.organization, norp = t."NORP"
        FROM temp_twit_comm_entity AS t
        WHERE f.id = t.id
    """

    with engine.begin() as conn:     # Transaction
        conn.exec_driver_sql(twitter_comment_sql)

'''Entity recognition for Twitter users'''
def get_user_org():
    user_org = []
    for ent in desc_tokens.ents:
        if ent.label_ == 'ORG':
            user_org.append(ent.text)
        if len(user_org) == 0:
            continue

    desc_df['user_organization'] = pd.Series(user_org)
    desc_df['user_organization'] = desc_df['user_organization'].astype(str)

def get_user_norp():
    user_norp = []
    for ent in desc_tokens.ents:
        if ent.label_ == 'NORP':
            user_norp.append(ent.text)
        if len(user_norp) == 0:
            continue

    desc_df['user_NORP'] = pd.Series(user_norp)
    desc_df['user_NORP'] = desc_df['user_NORP'].astype(str)

def upload_user_entity():
    desc_df.to_sql('twitter_user', con=engine, if_exists='replace',index=False)

    user_desc_sql = """
        UPDATE twitter_comments AS f
        SET user_organization = t.user_organization, user_NORP = t."user_NORP"
        FROM twitter_user AS t
        WHERE f.id = t.id
    """

    with engine.begin() as conn:     
        conn.exec_driver_sql(user_desc_sql)
