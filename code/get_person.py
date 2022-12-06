<<<<<<< HEAD
from database import engine 
from collections import Counter
from collections import defaultdict
from get_token import tokens
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

df = pd.read_sql_query(reddit_comments, engine)

df['comment'] = df['comment'].astype(str)

article = [x for x in df['comment']]

entities_by_article = []
for doc in nlp.pipe(article):
    people = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.append(ent)
    entities_by_article.append(people)


df['people'] = pd.Series(entities_by_article)
df['people'] = df['people'].astype(str)
print(len(df['people']), df)


with engine.connect() as connection:
  df.to_sql('temp_red_comm_entity', con=connection, if_exists='replace',index=False)


reddit_comment_sql = """
    UPDATE reddit_comments AS f
    SET people = t.people
    FROM temp_red_comm_entity AS t
    WHERE f.reddit_post_id = t.reddit_post_id
"""

with engine.begin() as conn:     # TRANSACTION
    conn.execute(reddit_comment_sql)

'''Entity recognition for Reddit posts'''

'''Entity recognition for Tweets''' 


'''Analysis: top entities'''

person_list = []
for ent in tokens.ents:
    if ent.label_ == 'PERSON':
        person_list.append(ent.text)
        
person_counts = Counter(person_list).most_common(20)
df_person = pd.DataFrame(person_counts, columns =['text', 'count'])

print('Length of df_person', len(df_person), df_person)

'''Analysis: top nationalities, religious, and political groups'''
norp_list = []
for ent in tokens.ents:
    if ent.label_ == 'NORP':
        norp_list.append(ent.text)
        
norp_counts = Counter(norp_list).most_common(20)
df_norp = pd.DataFrame(norp_counts, columns =['text', 'count'])

print('Length of df_norp', len(df_norp), df_norp)
=======
from database import engine 
from collections import Counter
from collections import defaultdict
from get_token import tokens
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

df = pd.read_sql_query(reddit_comments, engine)

df['comment'] = df['comment'].astype(str)

article = [x for x in df['comment']]

entities_by_article = []
for doc in nlp.pipe(article):
    people = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.append(ent)
    entities_by_article.append(people)


df['people'] = pd.Series(entities_by_article)
df['people'] = df['people'].astype(str)
print(len(df['people']), df)


# with engine.connect() as connection:
#   df.to_sql('temp_red_comm_entity', con=connection, if_exists='replace',index=False)


# reddit_comment_sql = """
#     UPDATE reddit_comments AS f
#     SET people = t.people
#     FROM temp_red_comm_entity AS t
#     WHERE f.reddit_post_id = t.reddit_post_id
# """

# with engine.begin() as conn:     # TRANSACTION
#     conn.execute(reddit_comment_sql)

'''Entity recognition for Reddit posts'''

'''Entity recognition for Tweets''' 


'''Analysis: top entities'''

person_list = []
for ent in tokens.ents:
    if ent.label_ == 'PERSON':
        person_list.append(ent.text)
        
person_counts = Counter(person_list).most_common(20)
df_person = pd.DataFrame(person_counts, columns =['text', 'count'])

print('Length of df_person', len(df_person), df_person)

'''Analysis: top nationalities, religious, and political groups'''
norp_list = []
for ent in tokens.ents:
    if ent.label_ == 'NORP':
        norp_list.append(ent.text)
        
norp_counts = Counter(norp_list).most_common(20)
df_norp = pd.DataFrame(norp_counts, columns =['text', 'count'])

print('Length of df_norp', len(df_norp), df_norp)
>>>>>>> 51dfd4c5ebde4f4c1d43a66973474edbc13bd412
