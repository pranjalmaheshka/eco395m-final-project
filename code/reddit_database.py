import csv
import os
import pandas as pd

INPUT_PATH_1 = os.path.join("artifacts", "reddit_posts_results.csv")
INPUT_PATH_2 = os.path.join("artifacts", "reddit_comments_results.csv")
OUTPUT_PATH_1 = os.path.join("uploads", "reddit_posts_results_upload.csv")
OUTPUT_PATH_2 = os.path.join("uploads", "reddit_comments_results_upload.csv")

def news_company():
	"""Get Reddit articles' news company names. Append news company names as an additional column to the csv."""

	with open (INPUT_PATH_1,'r', encoding="latin-1") as csv_file:
		reader = csv.reader(csv_file)
		next(reader) 

		company = []
		for row in reader:
			url = row[2]
			if url[8:12] == "www.":
				index_ = [] 
				index_count = 0
				for i in url:
					if i == ".":
						index_.append(index_count)
					index_count += 1
				company.append(url[index_[0]+1:index_[1]])
			else:
				index_ = []
				index_count = 0
				for i in url:
					if i == ".":
						index_.append(index_count)
					index_count += 1
				company.append(url[8:index_[0]])
		return company


def rating(company):
	"""Get Reddit articles' news company media bias rating. Append bias rating as an additional column to the csv."""

	ratings = []
	for i in company:
		if i in ("alternet", "theatlantic", "buzzfeednews", "cnn", "democracynow", "dailybeast", "huffpost", \
		"theintercept", "jacobin", "motherjones", "msnbc", "thenewyorker", "thenation", "slate", "vox", \
		"rollingstone","salon", "newrepublic", "esquire"):
			ratings.append(1)

		elif i in ("abcnews", "apnews", "bloomberg", "cbs", "theguardian", "insider", "nbcnews", "nytimes", "npr", \
		"politico", "propublica", "time", "washingtonpost", "usatoday", "yahoo", "businessinsider", "commondreams", \
		"indpendent"):
			ratings.append(2)

		elif i in ("axios", "bcc", "csmonitor", "forbes", "marketwatch", "newsnation", "newsweek", "reuters", \
		"realclearpolitics", "thehill", "wsj", "cnbc", "abc57", "kentucky"):
			ratings.append(3)

		elif i in ("thedispatch", "theepochtimes", "foxbusiness", "ijr", "nypost", "thepostmillenial", "reason", \
		"washingtonexaminer", "washingtontimes"):
			ratings.append(4)

		elif i in ("theamericanconservative", "spectator", "breitbart", "theblaze", "cbn", "dailycaller", \
		"dailymail", "dailywire", "foxnews", "thefederalist", "nationalreview", "newsmax", "freebeacon", "oann"):
			ratings.append(5)
	return ratings


def output():
	"""Export files as headerless csv files."""

	df1 = pd.read_csv (INPUT_PATH_1)
	df1["news company"] = news_company()
	df1["poltical rating"] = rating(news_company())
	df1["ranking"] = list(range(1, len(news_company())+1))
	df1.to_csv(OUTPUT_PATH_1, header=None,index=False)
	df2 = pd.read_csv (INPUT_PATH_2)
	df2.to_csv(OUTPUT_PATH_2, header=None,index=False)

	#df.to_csv("reddit_comment_results_upload.csv", index=False, header=False)

output()

































