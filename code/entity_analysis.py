from database import engine
from collections import Counter
from get_person import reddit_person
from get_person import reddit_norp
from get_person import reddit_org
from get_person import twitter_person
from get_person import twitter_norp
from get_person import twitter_org
from get_person import user_norp
from get_person import user_org
import pandas as pd
import spacy

"""Reddit Analysis: top entities"""
reddit_person_counts = Counter(reddit_person).most_common(30)
red_df_person = pd.DataFrame(reddit_person_counts, columns=["text", "count"])
red_df_person.to_sql("red_df_person", con=engine, if_exists="replace", index=False)

"""Reddit Analysis: top nationalities, religious, and political groups"""
reddit_norp_counts = Counter(reddit_norp).most_common(20)
red_df_norp = pd.DataFrame(reddit_norp_counts, columns=["text", "count"])
red_df_norp.to_sql("red_df_norp", con=engine, if_exists="replace", index=False)

"""Reddit Analysis: top organizations"""
reddit_org_counts = Counter(reddit_org).most_common(20)
red_df_org = pd.DataFrame(reddit_org_counts, columns=["text", "count"])
red_df_org.to_sql("red_df_org", con=engine, if_exists="replace", index=False)

"""Twitter Analysis: top entities"""
twitter_person_counts = Counter(twitter_person).most_common(20)
twitter_df_person = pd.DataFrame(twitter_person_counts, columns=["text", "count"])
twitter_df_person.to_sql(
    "twitter_df_person", con=engine, if_exists="replace", index=False
)

"""Twitter Analysis: top nationalities, religious, and political groups"""
twitter_norp_counts = Counter(twitter_norp).most_common(20)
twitter_df_norp = pd.DataFrame(twitter_norp_counts, columns=["text", "count"])
twitter_df_norp.to_sql("twitter_df_norp", con=engine, if_exists="replace", index=False)

"""Twitter Analysis: top organizations"""
twitter_org_counts = Counter(twitter_org).most_common(20)
twitter_df_org = pd.DataFrame(twitter_org_counts, columns=["text", "count"])
twitter_df_org.to_sql("twitter_df_org", con=engine, if_exists="replace", index=False)

"""Twitter Analysis: Twitter description"""
user_org_counts = Counter(user_org).most_common(20)
user_df_org = pd.DataFrame(user_org_counts, columns=["text", "count"])
user_df_org.to_sql("user_df_org", con=engine, if_exists="replace", index=False)

user_norp_counts = Counter(user_norp).most_common(20)
user_df_norp = pd.DataFrame(user_norp_counts, columns=["text", "count"])
user_df_norp.to_sql("user_df_norp", con=engine, if_exists="replace", index=False)
