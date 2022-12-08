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


# Step 1: Make sure GCP database instance is configured
scrape_reddit(50)
twitter_scraper()

# Step 2: Upload csv output in eco395m-final-project/artifacts
get_sentiment(?)
get_entity(?)

#Steo ?: Run get_person to analyse data and updata database with recognised entities
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

# Step 3: Data Visualization


if __name__ == "__main__":
    #
