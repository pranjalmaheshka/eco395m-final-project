## Main File
import os
import pandas as pd
from get_reddit import scrape_reddit
from get_twitter import twitter_scraper
from get_sentiment import get_sentiment
from get_person import get_reddit_people
from get_person import get_reddit_org
from get_person import get_reddit_norp
from get_person import get_twitter_people
from get_person import get_twitter_org
from get_person import get_twitter_norp
from get_person import get_twitter_norp
from get_person import get_user_org
from get_person import get_user_norp
from get_person import upload_reddit_entity
from get_person import upload_twitter_entity
from get_person import upload_user_entity
from dashboard import dashboard 


# Scrape Reddit and Twitter
scrape_reddit(50)
twitter_scraper()

# NLP Analysis
get_sentiment()
get_reddit_people()
get_reddit_org()
get_reddit_norp()
get_twitter_people()
get_twitter_org()
get_twitter_norp()
get_twitter_norp()
get_user_org()
get_user_norp()
upload_reddit_entity()
upload_twitter_entity()
upload_user_entity()

# Data Visualization
dashboard()
