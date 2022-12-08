<h1 align="center" id="heading"> <span style="color:red"> <em> Reddit versus Twitter </em> <br> Are polarized opinions the new normal? </span> </h1>
<h3 align="center" id="heading"> 8 December 2022 <br> 
<em> Python, Big Data, and Databases (ECO395m)  </em> <br> <h3>
<h3 align="center" id="heading"> Soo Jee Choi, Shreya Kamble, Pranjal Maheshka, Annie Nguyen, Tarini Sudhakar </h3>
  

 <h3> Introduction </h3> 
 
 This project analyzes bias and polarity in political discussions on Reddit and Twitter. The goal is to identify if there discussions on these websites lean in one direction or the other in terms of the sentiment and language used. For example, does Reddit usually more negative comments than Twitter for the same political conversation? Is there a prevalence for certain political viewpoints on either website?
 
 
 <p align="center"> 
 	<img src="https://github.com/pranjalmaheshka/eco395m-final-project/blob/main/uploads/giphy.gif" />
 </p>
 
 <h3> Methodology </h3> 
   We scraped Reddit and Twitter using APIs, added the post/comment information to a SQL database on Google Cloud Platform (GCP), and used SQL to query and analyse the data using Natural Language Processing (NLP) toolkits. The SQL databases were uploaded, and the data analysis outputs were shown using Streamlit. 
  
  1. _Scraping Reddit:_ We started by scraping the top 50 posts on the r/politics subreddit over the last month (November 2022), and the associated top comments for each of the posts. The data scraped included the main post and its score (upvotes), the url to the news article being discussed, the number of comments, and the top comments and their scores (upvotes). The output is pushed directly into a database. A sample of the output is saved as a csv in the /artifacts/ folder. 
  
  2. _Scraping Twitter:_ We used the headlines and url for the news articles from Reddit to search related posts on Twitter. We used snscrape to scrape tweets and their replies along with the number of likes and retweets for both to gauge the level of engagement. 
  
  3. _Natural Language Processing (NLP):_ We used the nltk (Vader) and spaCy packages on Python to analyze sentiments and entities in the posts and the comments scraped from both platforms. Vader assigns a positive, a neutral, and a negative sentiment value to each comment that sums to 1. We created a framework in order to rate the comments on an ordinal 1-5 scale where 1 - Very Negative, 2 - Negative, 3 - Neutral, 4- Positive, and 5 - Very Positive based off the raw sentiment scores provided by Vader. Named-Entity-Recognition in spaCy identifies different categories mentioned or found in the text. We use it to identify people, organisations, and nationalities or religious and political parties for Reddit, Twitter databases and Twitter users.    
  
<h3> Reproducing Code </h3> 

Install the necessary packages with pip install -r requirements.txt. Run `code/main.py' to successfully generate all the results. This is what will run in the background: 

  1. Creating a database: Make a PostgreSQL 13 database instance on GCP. Use GCP SQL to create a database called `reddit` that stores the scraped data from Reddit. Connect your database to a SQL editor of your choice (we used DBeaver). You can enter your credentials (host, username, database, and IP) in demo.env for establishing the connection.    
  
  2. Scrape Reddit: We used [PRAW](https://praw.readthedocs.io/en/stable/) to scrape the Politics category from Reddit. Enter credentials the same in demo.env. Run `code/scrape_reddit.py` to scrape the data and upload the outputs directly to the SQL database. We generate two tables: `reddit_posts` and `reddit_comments`. reddit_posts contains top 50 Reddit posts under the Politics thread with the reddit_post_id as the unique identifier. reddit_comments contains comments on each post. The same code/scrape_reddit.py also grabs the name of the news outlet and showcases where it lies on the political spectrum  based on [All Sides](https://www.allsides.com/media-bias/media-bias-chart) data.  
  
  3. Scrape Twitter: We used snscrape to scrape tweets and corresponding replies based on headlines and urls from Twitter. No credentials are required for this. Run `code/scrape_twitter.py` to scrape the Twitter data. The file loops through the reddit_posts table from the SQL database and scrapes tweets based on headlines and urls of news articles. The output is pushed to a separate table `twitter_comments` in the SQL database. 
  
  4. Get sentiment scores: We used the nltk (Vader) to calculate sentiment scores for Reddit and Twitter comments. Run `code/get_sentiment.py` for the same and upload scores to the SQL database. It updates the reddit_comments and twitter_comments table with sentiment scores for each post. It also generates three new tables: `reddit_site-results`, `twitter_site-results`, and `post_comparison`. The site-results table stores aggregate sentiment scores for Reddit and Twitter data. The post_comparison table contains a post-by-post comparison of sentiment scores for Reddit and Twitter. 
  
  5. Recognise entities: We used spaCy to recongise entities in the Reddit and Twitter data. We first generated tokens for the data in the `get_token.py`. After running that file, run `get_person.py` to store NLP-recognised people, organisations, and nationalities, or religious and political parties (NORP). `entity_analysis.py` calculates the top occurrences of each entity for the Reddit and Twitter data. We also included the analysis of the Twitter users description in these files. 
  
  6. Streamlit: Run `code/dashboard.py` to generate the dashboard for a visual representation of our results. It will open as a new tab in your browser. 
  
  
<h3> Results </h3> 

_How are people engaging with posts?_ 
	
  A sentiment analysis of Reddit comments showed the following split in sentiment. A majority of the comments are neutral while the positive and negative comments are distributed relatively evenly skewing towards the positive side. There are fewer upvotes on average for the very positive comments while the highest average upvotes are seen for negative comments. 

  Twitter sees about 60% of the comments leaning neutral and it has 50% more very positive comments compared to very negative comments. Once again, the negative comments have the highest engagement at 185 likes on average versus just 13 likes on average for the very positive comments. 
  
 <p align="center"> 
 	<img src="https://github.com/pranjalmaheshka/eco395m-final-project/blob/main/uploads/Sentiment.jpeg" />
 </p>
 
  Overall, the prevalence of neutral comments is a little surprising because we normally see different sections of the population use these social media platforms. Our general experience often sees more opinionated individuals online and we expected a greater bias away from neutral. 

  Comparing both the sites we can see that about 10% of the times there is significant difference in overall sentiment regarding a post (<0.20 points and the scaled score is on a [-1,1] scale). 

_What does frequently come up?_ 																       
	Biden is the most frequently mentioned person across Reddit and Twitter. Lauren Boebert is a close second on Reddit. Interestingly, Donald Trump comes up 87 times, and Jesus follows him with 84 mentions. Twitter data is not as clean as Reddit but we can see Donald Trump coming in second after Biden. 

Reddit clearly has more mentions of Republican-affiliated individuals when compared to Twitter. John Fetterman was the only Democrat that received mentions on both Reddit and Twitter. But Obama has the third-highest mentions of all individuals on Reddit.

When we look at NORP for the Reddit comments and tweets, Republicans were recognised 2057 times on Reddit. On the other hand, Democrats only received 1224 counts. On Twitter, Republicans get 183 counts. 161 Democrats were recognised. 

When we simply look at the Twitter users, we find 127—the largest group in all the user data—can be identified as Democrats. There are only 33 Republicans in comparison.

<h3> Limitations and Future Considerations </h3>
  Analyzing language has many inherent limitations given the how contextual conversations can be. Certain phrases and sentences may differ entirely in meaning from setting to the next. Discussions on social media can be hard to analyze even manually given tonal differences, sarcasm, and sometimes just grammatically incorrect or incoherent comments. 
	
  Software like Vader or spaCy can estimate sentiments and analyze entities in text but have limited power when it comes to language used online which includes slang, acronyms, and even emojis. Vader's rating system uses a dictionary-based approach for assigning positive, neutral, or negative sentiment scores. Consequently, a lot of comments averaged out to a neutral rating even though the overall sentiment might lean one way or the other. 

  We did not analyze the overall sentiment of the news articles themselves and could not identify if they had a political leaning. Accordingly, the sentiment analysis lacks a political viewpoint in seeing if the sites are biased towards one political ideology or another. 

  We also were not able to lemmatize the tokens generated using spaCy as it took too much memory space. That would clean the final results much more; for example, Republican and Republicans would be the same word. 
  
  Next steps could include analyzing the sentiment of the news article, identifying political biases in the news, checking to see the accuracy of the news reported relative to other reputable news publications, and then analyzing user sentiments and political biases. We can also analyse the sentiment regarding the recognised entities. Certain other considerations also include stringing together comments that are posted across multiple tweets on Twitter for a more thorough analysis of the sentiment. Shorter comments and tweets that are just a few words could be excluded, emojis can be dropped, and the sentiment analysis could include an expanded dictionary for Reddit and Twitter specific language. 
  
<h3> Conclusion </h3> 
	
  Overall, there does not seem to be a significant difference in positive or negative sentiments across Reddit and Twitter on a post or site level. The biggest difference is the prevalence of neutral comments. An interesting observation is that negative comments see the highest level of engagement on both platforms. Comparing posts across sites we see limited differences in sentiment for 10% of the posts. It is unclear what differentiates these posts in terms of poltiical bias or overall sentiment that could lead to these differences and that is an avenue for future analysis. 
