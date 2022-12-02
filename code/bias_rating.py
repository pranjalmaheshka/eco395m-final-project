import csv
import os

INPUT_PATH = os.path.join("artifacts", "reddit_posts_results.csv")

def news_company():
	"""Get Reddit articles' news company names. Append news company names as an additional column to the csv."""
	with open (INPUT_PATH,'r', encoding="latin-1") as csv_file:
		reader = csv.reader(csv_file)
		next(reader) 

		company = []
		for row in reader:
			url = row[2]
			if url[8:12] == "www.":
				index_ = [] #index of "."
				index_count = 0
				for i in url:
					if i == ".":
						index_.append(index_count)
					index_count += 1
				company.append(url[index_[0]+1:index_[1]])
			else:
				index_ = [] #index of "."
				index_count = 0
				for i in url:
					if i == ".":
						index_.append(index_count)
					index_count += 1
				company.append(url[8:index_[0]])
		print(count(company))
news_company()

#def rating()































