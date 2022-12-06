from database import engine 
from collections import Counter
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 10000000

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

df['parsed_comments'] = df['comment'].apply(lambda x: [y.lemma_ for y in nlp(x)])

print(df)

###Tokens 

tokens = nlp(''.join(str(df.parsed_comments.tolist())))

items = [x.text for x in tokens.ents]

c = Counter(items).most_common(50)

tok = pd.DataFrame.from_records(list(dict(c).items()), columns=['Token','Count'])

print('Length of tokens', len(tok), tok) 

###Entities 

person_list = []
for ent in tokens.ents:
    if ent.label_ == 'PERSON':
        person_list.append(ent.text)
        
person_counts = Counter(person_list).most_common(30)
df_person = pd.DataFrame(person_counts, columns =['text', 'count'])

print('Length of df_person', len(df_person), df_person)
