from database import engine 
from collections import defaultdict
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

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
#print(df)

df['comment'] = df['comment'].astype(str)

sample = df.sort_values(by=['comment']).head(5)
#print(sample)

article = [_ for _ in sample['comment']]
print(article)
#print(type(article))

for a in article:
 	doc = nlp(a)
#print(a)
#print(a)

# entities_by_article = []
# dic = defaultdict(list)

# for a in article:
# 	doc = nlp(a)
# 	people = []
# 	org = []
# 	for ent in doc.ents:
# 		if ent.label_ == "PERSON":
# 			people.append(ent)
# 		if ent.label_ == "ORG": 
# 			org.append(ent)
# 	dic['People'].append(people)
# 	dic['Organisation'].append(org)
# 	entities_by_article.append(dic)

# print(entities_by_article)

# check = pd.DataFrame(entities_by_article)
# check['People'] = check['People'].astype(str)
# check['Organisation'] = check['Organisation'].astype(str)

# print(check)
# print(check.dtypes)

# insert_entity = """
# insert into reddit_comments (people, organisation)
# VALUES (%(People)s, %(Organisation)s); 
# """

# with engine.connect() as connection:
# 	check.to_sql('reddit_comments', con=connection, if_exists='append',index=False)



