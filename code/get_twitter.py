import snscrape.modules.twitter as sntwitter

#from Reddit database take Twitter headlines and link 
# 1 article = 1 headline + 1 link 
#Take headline and link from Reddit dataset and store separately 
#From that list, run the text of headline and link in the two functions below 

def twitter_headlines(): 
	headlines_container = []

	for i,tweet in enumerate(sntwitter.TwitterSearchScraper('John Fetterman wins Pennsylvania Senate race, defeating TV doctor Mehmet Oz and flipping key state for Democrats').get_items()):
			if i>10:
				break
			headlines_container.append([tweet.date, tweet.user.username, tweet.content, tweet.url, tweet.id])
	print(headlines_container)

def twitter_urls(): 
	links_container = []

	for i,tweet in enumerate(sntwitter.TwitterSearchScraper('https://www.nbcnews.com/politics/2022-election/pennsylvania-senate-midterm-2022-john-fetterman-wins-election-rcna54935').get_items()):
			if i>200:
				break
			links_container.append([tweet.date, tweet.user.username, tweet.content, tweet.url, tweet.id])
	print(links_container)