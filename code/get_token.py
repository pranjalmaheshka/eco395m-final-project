<<<<<<< HEAD
from database import engine 
from collections import Counter
from collections import defaultdict
import pandas as pd
import spacy

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
#print(df)

df['comment'] = df['comment'].astype(str)

tokens = nlp(''.join(str(df.comment.tolist())))

items = [x.text for x in tokens.ents]

c = Counter(items).most_common(50)

df = pd.DataFrame.from_records(c.most_common(), columns=['Token','Count'])

print('Length of tokens', len(df), df) 
=======
from database import engine 
from collections import Counter
from collections import defaultdict
import pandas as pd
import spacy

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
#print(df)

df['comment'] = df['comment'].astype(str)

tokens = nlp(''.join(str(df.comment.tolist())))

items = [x.text for x in tokens.ents]

c = Counter(items).most_common(50)

#df = pd.DataFrame.from_records(c.most_common(), columns=['Token','Count'])

print('Length of tokens', len(c), c) 
>>>>>>> 51dfd4c5ebde4f4c1d43a66973474edbc13bd412
