from data_analysis import *
import streamlit as st
import matplotlib.pyplot as plt



def wordcloud_platform(platform):
	'''Take user inputted Platform and Entity and returns formatted WordCloud'''
	fig, ax = plt.subplots(figsize = (20, 10)) 
	plt.axis("off")
	plt.tight_layout(pad=0)
	if platform == "Reddit People":
		ax.imshow(wc_reddit_people(), interpolation='bilinear')

	elif platform == "Twitter People":
		ax.imshow(wc_twitter_people(), interpolation='bilinear')

	elif platform == "Reddit Norp":
		ax.imshow(wc_reddit_norp(), interpolation='bilinear')

	elif platform == "Twitter Norp":
		ax.imshow(wc_twitter_norp(), interpolation='bilinear')

	elif platform == "Reddit Organization":
		ax.imshow(wc_reddit_org(), interpolation='bilinear')

	elif platform == "Twitter Organization":
		ax.imshow(wc_twitter_org(), interpolation='bilinear')
	return st.pyplot(fig)








# def wordcloud_platform(platform):
# 	'''Take user inputted Platform and Entity'''
# 	if platform == "Reddit People":
# 		fig, ax = plt.subplots(figsize = (20, 10)) 
# 		plt.axis("off")
# 		plt.tight_layout(pad=0)
# 		ax.imshow(wc_reddit_people(), interpolation='bilinear')
# 		return st.pyplot(fig)

# 	elif platform == "Twitter People":
# 		fig, ax = plt.subplots(figsize = (20, 10)) 
# 		plt.axis("off")
# 		plt.tight_layout(pad=0)
# 		ax.imshow(wc_twitter_people(), interpolation='bilinear')
# 		return st.pyplot(fig)

# 	if platform == "Reddit Norp":
# 		fig, ax = plt.subplots(figsize = (20, 10)) 
# 		plt.axis("off")
# 		plt.tight_layout(pad=0)
# 		ax.imshow(wc_reddit_norp(), interpolation='bilinear')
# 		return st.pyplot(fig)

# 	elif platform == "Twitter Norp":
# 		fig, ax = plt.subplots(figsize = (20, 10)) 
# 		plt.axis("off")
# 		plt.tight_layout(pad=0)
# 		ax.imshow(wc_twitter_norp(), interpolation='bilinear')
# 		return st.pyplot(fig)

# 	if platform == "Reddit Organization":
# 		fig, ax = plt.subplots(figsize = (20, 10)) 
# 		plt.axis("off")
# 		plt.tight_layout(pad=0)
# 		ax.imshow(wc_reddit_org(), interpolation='bilinear')
# 		return st.pyplot(fig)

# 	elif platform == "Twitter Organization":
# 		fig, ax = plt.subplots(figsize = (20, 10)) 
# 		plt.axis("off")
# 		plt.tight_layout(pad=0)
# 		ax.imshow(wc_twitter_org(), interpolation='bilinear')
# 		return st.pyplot(fig)

def build():
	'''Build Streamlit Dashboard'''
	st.set_page_config(layout='wide')
	hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
	st.markdown(hide_table_row_index, unsafe_allow_html=True)
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.image("header.png")
	st.title ("Analyzing Political Sentiment Across Social Media Platforms")
	st.header("Reddit vs Twitter")
	st.markdown("***")

	st.write("")
	st.subheader("Top 10 'Politics' Subreddit Posts This Month")
	st.table(top_posts())
	st.markdown("***")

	st.subheader("Media Bias Score")
	st.write("Chart displays the Media Bias Ratings of the Top 50 Reddit Posts this Month.")
	st.write("*Media Bias Ratings come from the AllSides Media Bias Ratings and Chart")
	st.write("N = 50 | 1 = Left, 2 = Lean Left, 3 = Center, 4 = Lean Right, 5 = Right")
	st.write("")
	st.write("")
	st.altair_chart(media_bias_rating()) 
	st.write("")
	st.markdown("***")

	st.write("")
	st.write("")
	st.subheader("Search the Top 50 Politics Posts")
	st.write("Enter the rank of the Reddit 'Politics' post you would like to see.")
	st.write("Ex: The value '1' displays the top post.")
	num = st.number_input("Enter a value between 1 and 50:", min_value=1, max_value=50)
	st.write("")
	st.write("__Title__: ", post_query(num)[1])
	st.write("__Link:__ ", post_query(num)[3])
	st.write("__Date Posted:__ ", post_query(num)[2])
	st.write("__Upvotes:__ ", post_query(num)[4])
	st.write("__Comments:__ ", post_query(num)[5])
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.markdown("***")

	st.subheader("Explore the Top Article Responses By Platform")
	st.write("Select the Article and Social Media Platform you would like to view.")
	num = st.slider("Use the Slider to Select an Article based on it's Ranking" , min_value=1, max_value=50)
	platform = st.radio("Social Media Platform",["Reddit","Twitter"])
	if platform == "Reddit":
		st.write("")
		st.write("__Article:__ ", post_query(num)[1])
		st.write("__Top 5 Most Liked Comments__: ")
		st.write("__1.__ ", reddit_top_comments(num)[0][0])
		st.write("__Likes__: ", reddit_top_comments(num)[1][0])
		st.write("")
		st.write("__2.__ ", reddit_top_comments(num)[0][1])
		st.write("__Likes__: ", reddit_top_comments(num)[1][1])
		st.write("")
		st.write("__3.__ ", reddit_top_comments(num)[0][2])
		st.write("__Likes__: ", reddit_top_comments(num)[1][2])
		st.write("")
		st.write("__4.__ ", reddit_top_comments(num)[0][3])
		st.write("__Likes__: ", reddit_top_comments(num)[1][3])
		st.write("")
		st.write("__5.__ ", reddit_top_comments(num)[0][4])
		st.write("__Likes__: ", reddit_top_comments(num)[1][4])
		st.write("")
	if platform == "Twitter":
		st.write("")
		st.write("__Article:__ ", post_query(num)[1])
		st.write("__Top 5 Most Liked Tweets__: ")
		st.write("__1.__ ", twitter_top_comments(num)[0][0])
		st.write("__Likes__: ", twitter_top_comments(num)[1][0])
		st.write("")
		st.write("__2.__ ", twitter_top_comments(num)[0][1])
		st.write("__Likes__: ", twitter_top_comments(num)[1][1])
		st.write("")
		st.write("__3.__ ", twitter_top_comments(num)[0][2])
		st.write("__Likes__: ", twitter_top_comments(num)[1][1])
		st.write("")
		st.write("__4.__ ", twitter_top_comments(num)[0][3])
		st.write("__Likes__: ", twitter_top_comments(num)[1][3])
		st.write("")
		st.write("__5.__ ", twitter_top_comments(num)[0][4])
		st.write("__Likes__: ", twitter_top_comments(num)[1][4])
		st.write("")
	st.markdown("***")

	st.write("")
	st.write("")
	st.subheader("Article Ranking Comparison")
	st.write("Popularity Ranking of the Top 50 'Politics' Reddit Articles by Platform.")
	st.write("")
	st.write("")
	st.write("")
	st.altair_chart(rank_comparison())
	st.write("")
	st.write("")
	st.markdown("***")

	st.subheader("NLP Sentiment Analysis Results")
	st.markdown(hide_table_row_index, unsafe_allow_html=True)
	st.table(sentiment_analysis())
	st.write("")
	st.write("")
	st.write("1 = Very Negative, 2 = Negative, 3 = Neutral, 4 = Positive, 5 = Very Positive")
	st.write("")
	st.write("")
	col1, col2 = st.columns(2)
	with col1:
		st.write("__Reddit Sentiment Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(reddit_sentiment())
		st.markdown("***")

	with col2:
		st.write("__Twitter Sentiment Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(twitter_sentiment())
		st.markdown("***")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.altair_chart(comparison())
	st.markdown("***")
	
	st.write("")
	st.write("")
	st.subheader("NLP Entity Analysis Results")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	col1, col2 = st.columns(2)
	with col1:
		st.write("__Reddit Top 20 People Entity Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(reddit_people())
	with col2:
		st.write("__Twitter Top 20 People Entity Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(twitter_people())
	st.write("")
	st.write("")
	st.markdown("***")

	st.write("")
	st.write("")
	col1, col2 = st.columns(2)
	with col1:
		st.write("__Reddit Top 20 Norp Entity Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(reddit_norp())
	with col2:
		st.write("__Twitter Top 20 Norp Entity Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(twitter_norp())
	st.write("")
	st.write("")
	st.markdown("***")

	st.write("")
	st.write("")
	col1, col2 = st.columns(2)
	with col1:
		st.write("__Reddit Top 20 Organization Entity Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(reddit_org())
	with col2:
		st.write("__Twitter Top 20 Organization Entity Analysis Distribution__")
		st.write("")
		st.write("")
		st.altair_chart(twitter_org())
	st.write("")
	st.write("")
	st.markdown("***")

	st.subheader("Top Words in Responses")
	st.write("Use the Select Box to view the World Cloud of the Top 20 Words in the Comments of each Social Media Platform.")
	st.write("")
	tab1, tab2, tab3 = st.tabs(["People", "Norp", "Organization"])
	with tab1:
		wc_platform = st.selectbox("Social Media Platform and Entity:",["Reddit People", "Twitter People"])
		wordcloud_platform(wc_platform)
	with tab2:
		wc_platform = st.selectbox("Social Media Platform:",["Reddit Norp", "Twitter Norp"])
		wordcloud_platform(wc_platform)
	with tab3:
		wc_platform = st.selectbox("Social Media Platform:",["Reddit Organization", "Twitter Organization"])
		wordcloud_platform(wc_platform)

	st.markdown("***")





	

	











if __name__ == "__main__":
	build()


