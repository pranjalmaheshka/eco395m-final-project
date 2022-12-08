<h1 align="center" id="heading"> <span style="color:red"> <em> Reddit Vs Twitter </em> <br> Are polarized opinions the new normal? </span> </h1>
<h3 align="center" id="heading"> 8 December 2022 <br> 
<em> Python, Big Data, and Databases (ECO395m)  </em> <br> <h3>
<h3 align="center" id="heading"> Soo Jee Choi, Shreya Kamble, Pranjal Maheshka, Annie Nguyen, Tarini Sudhakar </h3>
  

 <h3> Introduction </h3> 
 
 This project analyzes bias and polarity in political discussions on Reddit and Twitter. The goal is to identify if there discussions on these websites lean in one direction or the other in terms of the sentiment and language used. For example, does Reddit usually more negative comments than Twitter for the same political conversation? Is there a prevalence for certain political viewpoints on either website?
  
 <h3> Methodology </h3> 
   We scraped Reddit and Twitter using APIs, added the post/comment information to a database on Google Cloud Platform (GCP), and used SQL to query and analyse the data using Natural Language Processing (NLP) toolkits. The SQL databases were uploaded, and the data analysis outputs were shown using Streamlit. 
  
  1.Scraping Reddit: We started by scraping the top 50 posts on the r/politics subreddit over the last month (November 2022), and the associated top comments for each of the posts. The data scraped included the main post and its score (upvotes), the url to the news article being discussed, the number of comments, and the top comments and their scores (upvotes). The output is pushed directly into a database. A sample of the output is saved as a csv in the /artifacts/ folder. 
  
  2. Scraping Twitter: We used the headlines and url for the news articles from Reddit to search related posts on Twitter. We used snscrape to scrape tweets and their replies along with the number of likes and retweets for both to gauge the level of engagement. 
  
  3. Natural Language Processing: We used the nltk (Vader) and spaCy packages on python to analyze sentiments and entities in the posts and the comments scraped from both platforms. Vader assigns a positive, a neutral, and a negative sentiment value to each comment that sums to 1. We created a framework in order to rate the comments on an ordinal 1-5 scale where 1 - Very Negative, 2 - Negative, 3 - Neutral, 4- Positive, and 5 - Very Positive based off the raw sentiment scores provided by Vader.  
  
<h3> Reproducing Code CHECK SECTION</h3> 
  1. Database for Reddit: Set up a database instance on Google Cloud Platform (GCP) and create a databases for Reddit. Connect your database to a SQL editor of your choice.
  
  2. Scrape Reddit: Run code/scrape_reddit.py and then upload the outputs directly onto the database. 
  
  3. Scrape Twitter: Run code/scrape_twitter.py. The file loops through the reddit_posts table from the database and scrapes tweets based on headlines and urls of news articles. The output is pushed to a separate table in the database.
  
  4. NLP Analysis: 
  
  5. Streamlit: 
  
  
<h3> Results </h3> 
  A sentiment analysis of Reddit comments showed the following split in sentiment. A majority of the comments are neutral while the positive and negative comments are  distributed relatively evenly. 
  
  This is a little surprising because we normally see different sections of the population use these social media platforms. We expected some bias away from neutral overall given the prevalence of negative information and negative comments online. Looking at the po;ularity of comments itself we see that ...
  
<h3> Limitations </h3>
  Analyzing language has many inherent limitations given the how contextual conversations can be. Certain phrases and sentences may differ entirely in meaning from setting to the next. Discussions on social media can be hard to analyze even manually given tonal differences, sarcasm, and sometimes just grammatically incorrect or incoherent comments. Software like Vader or spaCy can estimate sentiments and analyze entities in text but have limited power when it comes to language used online which includes slang, aconyms, and even emojis. Vader's rating system uses a dictionary based approach for assigning positive, neutral, or negative sentiment scores. Consequently, a lot of comments averaged out to a neutral rating even though the overall sentiment might lean one way or the other. 
  
  
<h3> Conclusion </h3> 
  Overall there does not seem to be a significant difference in positive or negative sentiments across Reddit and Twitter on a post or site level. About half the comments are neutral in their language and the rest are equal parts split between negative and positive. About a quarter of the total comments could be classified as very negative or very positive but this does not lean in one direction. The conversations seem to be balanced overall and there is no clear bias. 
  There is a lot of scope for future updates to this project. 
  
