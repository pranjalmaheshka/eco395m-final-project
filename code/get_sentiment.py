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

df['comment'] = df['comment'].astype(str)

sample = df.sort_values(by=['comment']).head(5)
print(sample)

article = article = [_ for _ in sample['comment']]

entities_by_article = []
dic = defaultdict(list)

for a in article:
	doc = nlp(a)
	people = []
	org = []
	for ent in doc.ents:
		if ent.label_ == "PERSON":
			people.append(ent)
		if ent.label_ == "ORG": 
			org.append(ent)
	dic['People'].append(people)
	dic['Organisation'].append(org)
	entities_by_article.append(dic)

print(entities_by_article)

check = pd.DataFrame(entities_by_article)

print(check)


insert_entity = """
ALTER TABLE checkdata 
ADD people, organisation varchar;
"""

with engine.connect() as connection:
	check.to_sql('checkdata', con=connection, if_exists='append')

#for row in range(len(df)): 
#	doc = nlp(df.loc[row, 'comments']) 

# for i in doc.ents:  
# 	print[(i.text, i.label_)]

#print([(i.text, i.label_) for i in doc.ents])
#doc = nlp("BMan I can't wait to hear all the crazy laws Fetterman will pass according to my Fox News loving coworkers.  Edit: Holy shit didn't think this would blow up. Thank you and apologies for not responding to comments.")
#doc2 = nlp("YES THANK YOU PENNSYLVANIA. You all showed up!! Fetterman will be my favorite Senator in Congress now. Oz can move back to New Jersey and hopefully fade away into obscurity now.")

#print(test)
#print([(X.text, X.label_) for X in doc2.ents])

