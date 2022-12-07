from database import engine 
from collections import Counter
from get_person import reddit_person
from get_person import reddit_norp
from get_person import reddit_org
from get_person import twitter_person
from get_person import twitter_norp
from get_person import twitter_org
import pandas as pd
import spacy

######REDDIT
'''Analysis: top entities'''

reddit_person_counts = Counter(reddit_person).most_common(30)
red_df_person = pd.DataFrame(reddit_person_counts, columns =['text', 'count'])

print('Length of red_df_person', len(red_df_person), red_df_person)

'''Analysis: top nationalities, religious, and political groups'''
        
reddit_norp_counts = Counter(reddit_norp).most_common(20)
red_df_norp = pd.DataFrame(reddit_norp_counts, columns =['text', 'count'])

print('Length of red_df_norp', len(red_df_norp), red_df_norp)

'''Analysis: top organizations'''
        
reddit_org_counts = Counter(reddit_org).most_common(20)
red_df_org = pd.DataFrame(reddit_org_counts, columns =['text', 'count'])

print('Length of red_df_org', len(red_df_org), red_df_org)

######TWITTER
'''Analysis: top entities'''
        
twitter_person_counts = Counter(twitter_person).most_common(20)
twitter_df_person = pd.DataFrame(twitter_person_counts, columns =['text', 'count'])

print('Length of twitter_person_counts', len(twitter_df_person), twitter_df_person)

'''Analysis: top nationalities, religious, and political groups'''
        
twitter_norp_counts = Counter(twitter_norp).most_common(20)
twitter_df_norp = pd.DataFrame(twitter_norp_counts, columns =['text', 'count'])

print('Length of twitter_df_norp', len(twitter_df_norp), twitter_df_norp)


'''Analysis: top organizations'''

twitter_org_counts = Counter(twitter_org).most_common(20)
twitter_df_org = pd.DataFrame(twitter_org_counts, columns =['text', 'count'])

print('Length of twitter_df_org', len(twitter_df_org), twitter_df_org)


