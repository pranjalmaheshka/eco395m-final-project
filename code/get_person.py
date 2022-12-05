from database import engine 
from collections import Counter
from collections import defaultdict
import pandas as pd
import spacy

'''Entity recognition for Reddit comments'''
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 5000000
text = """
select 
    reddit_post_id, 
    comment
from 
    reddit_comments rc
group by 
    rc.reddit_post_id, rc.comment
"""

df = pd.read_sql_query(text, engine)

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
  df.to_sql('temp_entity', con=connection, if_exists='replace',index=False)


sql = """
    UPDATE reddit_comments AS f
    SET people = t.people
    FROM temp_entity AS t
    WHERE f.reddit_post_id = t.reddit_post_id
"""

with engine.begin() as conn:     # TRANSACTION
    conn.execute(sql)

'''Analysis'''


# person_counts = Counter(person_list).most_common(50)
# df_person = pd.DataFrame(person_counts, columns =['Person', 'Count'])

# print('This is person_list', len(person_list), person_list)
