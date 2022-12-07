## Main File
import os
import pandas as pd
from get_reddit import scrape_reddit
from get_twitter import twitter_scraper
from get_sentiment import get_sentiment
from get_entity import get_entity

# Step 1: Make sure GCP database instance is configured
scrape_reddit(50)
twitter_scraper()

# Step 2: Upload csv output in eco395m-final-project/artifacts
get_sentiment(?)
get_entity(?)

# Step 3: Data Visualization


if __name__ == "__main__":
    #
