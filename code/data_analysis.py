import os
from database import engine
import pandas as pd
import altair as alt
from wordcloud import WordCloud

def top_posts():
    '''Query top posts'''
    query = """
        select title, date_posted, post_score, num_comments, rank from reddit_posts
        where rank between 1 and 10;
    """
    df = pd.read_sql_query(query, engine)
    df = df[["rank", "title", "date_posted", "post_score", "num_comments"]]
    df.rename(columns={"rank": "Ranking", "title": "Title", "date_posted": "Date", "post_score": "Upvotes", "num_comments": "Comments"}, inplace=True)
    df = df.astype({"Ranking": "str", "Upvotes":"int","Comments":"int"})
    df = df.style.set_properties(**{'text-align': 'left'})
    return df


def media_bias_rating():
    '''Count of Media Bias rating scores of Top 50 'Politics' posts'''
    query = """
        select bias_rating from reddit_posts;
    """
    df = pd.read_sql_query(query, engine)

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0

    for i in df["bias_rating"].tolist():
        if i == 1:
            count1 += 1
        elif i == 2:
            count2 += 1
        elif i == 3:
            count3 += 1
        elif i == 4:
            count4 += 1
        elif i == 5:
            count5 += 1

    df = pd.DataFrame({
        "Media Bias Rating": ["1", "2", "3", "4", "5"], 
        "Count of Articles": [count1, count2, count3, count4, count5]})
    bar_chart = alt.Chart(df).mark_bar().encode(
            x = "Media Bias Rating",
            y = "Count of Articles",).properties(width=1000, height=400)
    return bar_chart


def post_query(num):
    '''Get article information by user inputted rank value'''
    query = """
        select title, date_posted, url, post_score, num_comments, rank from reddit_posts;
    """
    df = pd.read_sql_query(query, engine)
    df = df.loc[df["rank"] == num]
    title = df.loc[num-1, "title"]
    date = str(df.loc[num-1, "date_posted"])
    url = df.loc[num-1, "url"]
    upvotes = str(int(df.loc[num-1, "post_score"]))
    comments = str(int(df.loc[num-1, "num_comments"]))

    output = [num, title, date, url, upvotes, comments]
    return output


def reddit_top_comments(num):
    '''Get top 5 reddit comments for user inputted rank value'''
    reddit_top_five_comments = """
        with cte as (select title, rank as article_rank from reddit_posts)
        select a.title, a.comment, a.upvotes, a.rank, b.article_rank from (select * from 
        (select title, comment, upvotes,row_number() over(partition by title order by upvotes desc) rank
        from reddit_comments order by title, rank) p where rank <= 5 order by title) a
        left join cte b on b.title=a.title order by b.article_rank, a.rank;
    """
    df = pd.read_sql_query(reddit_top_five_comments, engine) 

    text_1 = df.loc[(df["article_rank"] == num) & (df["rank"] == 1), "comment"].item()
    text_2 = df.loc[(df["article_rank"] == num) & (df["rank"] == 2), "comment"].item()
    text_3 = df.loc[(df["article_rank"] == num) & (df["rank"] == 3), "comment"].item()
    text_4 = df.loc[(df["article_rank"] == num) & (df["rank"] == 4), "comment"].item()
    text_5 = df.loc[(df["article_rank"] == num) & (df["rank"] == 5), "comment"].item()

    like_1 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 1), "upvotes"].item()))
    like_2 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 2), "upvotes"].item()))
    like_3 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 3), "upvotes"].item()))
    like_4 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 4), "upvotes"].item()))
    like_5 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 5), "upvotes"].item()))

    return [[text_1, text_2, text_3, text_4, text_5], [like_1, like_2, like_3, like_4, like_5]]


def twitter_top_comments(num):
    '''Get top 5 Twitter Tweets based on user inputted rank value'''
    twitter_top_five_comments = """
        with cte as (select title, rank as article_rank from reddit_posts)
        select a.title, a.tweet, a.likes, a.rank, b.article_rank from 
        (select * from (select title, tweet, likes,row_number() over(partition by title order by likes desc) rank
        from twitter_comments order by title, rank) p where rank <= 5 order by title, rank) a
        left join cte b on b.title=a.title order by b.article_rank, a.rank;
    """
    df = pd.read_sql_query(twitter_top_five_comments, engine) 

    text_1 = df.loc[(df["article_rank"] == num) & (df["rank"] == 1), "tweet"].item()
    text_2 = df.loc[(df["article_rank"] == num) & (df["rank"] == 2), "tweet"].item()
    text_3 = df.loc[(df["article_rank"] == num) & (df["rank"] == 3), "tweet"].item()
    text_4 = df.loc[(df["article_rank"] == num) & (df["rank"] == 4), "tweet"].item()
    text_5 = df.loc[(df["article_rank"] == num) & (df["rank"] == 5), "tweet"].item()

    like_1 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 1), "likes"].item()))
    like_2 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 2), "likes"].item()))
    like_3 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 3), "likes"].item()))
    like_4 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 4), "likes"].item()))
    like_5 = str(int(df.loc[(df["article_rank"] == num) & (df["rank"] == 5), "likes"].item()))

    return [[text_1, text_2, text_3, text_4, text_5], [like_1, like_2, like_3, like_4, like_5]]


def rank_comparison():
    '''Get Reddit and Twitter article rankings of the Top 50 'Politics' posts based on upvotes and likes, respectively'''
    query = """
        with cte as (select title, likes, row_number() over(order by likes desc) overall_ranking 
        from (with cte as (select title, likes, row_number() over(partition by title order by likes desc) likes_ranking
        from twitter_comments)
        select title, likes from cte where likes_ranking = 1 order by likes desc) limiting)
        select a.overall_ranking as t_ranking, b.rank as r_ranking, a.likes as t_likes, b.post_score as r_likes, a.title, b.title 
        from (select title, post_score, rank from reddit_posts) b
        left join cte a on b.title=a.title order by r_ranking;
    """
    df = pd.read_sql_query(query, engine)
    df = pd.DataFrame({
    "Reddit Ranking": df["r_ranking"].tolist(),
    "Twitter Ranking": df["t_ranking"].tolist(),
    "Reddit Likes": df["r_likes"].tolist(),
    "Twitter Likes": df["t_likes"].tolist(),
    "x_line": range(1, 51),
    "y_line": range(1, 51),})

    chart = alt.Chart(df).mark_point().encode(
    x="Reddit Ranking",
    y="Twitter Ranking",
    color = alt.Color("Twitter Likes:N", legend=None),
    size = "Reddit Likes",)
    reflection_line = alt.Chart(df).mark_line().encode(
    x=alt.Y("x_line", axis=alt.Axis(title="Reddit Ranking")),
    y=alt.Y("y_line", axis=alt.Axis(title="Twitter Ranking")),).properties(width=1000, height=400) 

    final_chart = chart + chart.transform_regression("Reddit Ranking", "Twitter Ranking").mark_line() + reflection_line
    return final_chart

def wordcloud_input(df):
    '''Return string of words separated by commas for WordCloud input'''
    text = df["text"].tolist()
    count = df["count"].tolist()
    wordcloud_input = ""

    for i in range(0, len(text)):
        wordcloud_input += ((text[i] + ", ") * count[i])
    wordcloud_input = wordcloud_input[:-2]
    return wordcloud_input

def word_cloud_output(top_words):
    '''Output formatted WordCloud using the top words'''
    return WordCloud(width=2000, height=800, background_color="white").generate(top_words)

def wc_reddit_people():
    '''Reddit people entity query and wordcloud output'''
    query = """
        select * from red_df_person;
    """
    return word_cloud_output(wordcloud_input(pd.read_sql_query(query, engine)))

def wc_twitter_people():
    '''Twitter people entity query and wordcloud output'''
    query = """
        select * from twitter_df_person;
    """
    return word_cloud_output(wordcloud_input(pd.read_sql_query(query, engine)))

def wc_reddit_norp():
    '''Reddit norp entity query and wordcloud output'''
    query = """
        select * from red_df_norp;
    """
    return word_cloud_output(wordcloud_input(pd.read_sql_query(query, engine)))

def wc_twitter_norp():
    '''Twitter norp entity query and wordcloud output'''
    query = """
        select * from twitter_df_norp;
    """
    return word_cloud_output(wordcloud_input(pd.read_sql_query(query, engine)))

def wc_reddit_org():
    '''Reddit organization entity query and wordcloud output'''
    query = """
        select * from red_df_org;
    """
    return word_cloud_output(wordcloud_input(pd.read_sql_query(query, engine)))

def wc_twitter_org():
    '''Twitter organization entity query and wordcloud output'''
    query = """
        select * from twitter_df_org;
    """
    return word_cloud_output(wordcloud_input(pd.read_sql_query(query, engine)))

def entity_chart(df):
    '''Create bar graph for entity analysis'''
    text = df["text"].tolist()
    count = df["count"].tolist()
    df_chart = pd.DataFrame({
        "x": text,
        "y": count})
    chart = alt.Chart(df_chart).mark_bar().encode(
    x = alt.X("x", axis=alt.Axis(title="Top 20 Words")),
    y = alt.Y("y", axis=alt.Axis(title=" Count"),)).properties(width=600, height=400)

    return chart

def reddit_people():
    '''Reddit people entity query and chart output'''
    query = """
        select * from red_df_person;
    """
    return entity_chart(pd.read_sql_query(query, engine))

def twitter_people():
    '''Twitter people entity query and chart output'''
    query = """
        select * from twitter_df_person;
    """
    return entity_chart(pd.read_sql_query(query, engine))

def reddit_norp():
    '''Reddit norp entity query and chart output'''
    query = """
        select * from red_df_norp;
    """
    return entity_chart(pd.read_sql_query(query, engine))

def twitter_norp():
    '''Twitter norp entity query and chart output'''
    query = """
        select * from twitter_df_norp;
    """
    return entity_chart(pd.read_sql_query(query, engine))

def reddit_org():
    '''Reddit organization entity query and chart output'''
    query = """
        select * from red_df_org;
    """
    return entity_chart(pd.read_sql_query(query, engine))

def twitter_org():
    '''Twitter organization entity query and chart output'''
    query = """
        select * from twitter_df_org;
    """
    return entity_chart(pd.read_sql_query(query, engine))

def reddit_sentiment():
    query = """
        select * from  "reddit_site-results";
    """
    df = pd.read_sql_query(query, engine)
    x = ["1", "2", "3", "4", "5"]
    y = df["Sentiment Count"].tolist()
    df = pd.DataFrame({
        "x": x,
        "y": y})
    chart = alt.Chart(df).mark_bar().encode(
    x = alt.X('x', axis=alt.Axis(title="Sentiment Score")),
    y = alt.Y('y', axis=alt.Axis(title="Sentiment Count"),)).properties(width=600, height=400)
    return chart

def twitter_sentiment():
    query = """
        select * from  "twitter_site-results";
    """
    df = pd.read_sql_query(query, engine)
    x = ["1", "2", "3", "4", "5"]
    y = df["Sentiment Count"].tolist()
    df = pd.DataFrame({
        "x": x,
        "y": y})
    chart = alt.Chart(df).mark_bar().encode(
    x = alt.X('x', axis=alt.Axis(title="Sentiment Score")),
    y = alt.Y('y', axis=alt.Axis(title="Sentiment Count"),)).properties(width=600, height=400)
    return chart

def comparison():
    query = """
        select * from (with cte as (select "Post ID", "Reddit Score", "Twitter Score", abs("Diff") as diff from post_comparison 
        order by diff desc)
        select a."Reddit Score", a."Twitter Score", a."diff",a."Post ID", b.rank, b.reddit_post_id from (select title, rank, 
        reddit_post_id from reddit_posts) b left join cte a on a."Post ID"=b.reddit_post_id) query where diff is not 
        null order by diff desc limit 3;
    """
    df = pd.read_sql_query(query, engine)
    reddit = df["Reddit Score"].tolist()
    twitter = df["Twitter Score"].tolist()
    rank = df["rank"].tolist()

    df = pd.DataFrame([["Article Ranking: "+[rank[0], reddit[0], "Reddit"], 
                   ["Article Ranking: "+[rank[0], twitter[0], "Twitter"], 
                   ["Article Ranking: "+[rank[1], reddit[1], "Reddit"], 
                   ["Article Ranking: "+[rank[1], twitter[1], "Twitter"],
                   ["Article Ranking: "+[rank[2], reddit[2], "Reddit"], 
                   ["Article Ranking: "+[rank[2], twitter[2], "Twitter"]], 
                  columns=["Ranking", "Score", "Media"])

    chart = Chart(df).mark_bar().encode(
   column=Column('Genre'),
   x=X('Gender'),
   y=Y('Rating')

    df_chart = pd.DataFrame({
        "x": text,
        "y": count})
    chart = alt.Chart(df_chart).mark_bar().encode(
    x = alt.X("x", axis=alt.Axis(title="Top 20 Words")),
    y = alt.Y("y", axis=alt.Axis(title=" Count"),)).properties(width=600, height=400)

    return chart






def sentiment_analysis():

    results = {
    "Sentiment": ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"], 
    "Reddit Sentiment Count": [1.1234567, 2.2345678, 3.3456789, 4.4567890, 5.098765432],
    "Twitter Sentiment Count": [1.1234567, 2.2345678, 3.3456789, 4.4567890, 5.098765432],
    "Reddit Total Upvotes": [1.1234567, 2.2345678, 3.3456789, 4.4567890, 5.098765432],
    "Twitter Total Upvotes": [1.1234567, 2.2345678, 3.3456789, 4.4567890, 5.098765432],
    "Reddit Avg Upvotes": [1.1234567, 2.2345678, 3.3456789, 4.4567890, 5.098765432],
    "Twitter Avg Upvotes": [1.1234567, 2.2345678, 3.3456789, 4.4567890, 5.098765432]}

    return(pd.DataFrame(results))























    # df = pd.DataFrame({
    # 'strike': [-200,-225,250,275,300,325,-350,200,225,250,275,-300,325,350],
    # 'opttype': ['ce','ce','ce','ce','ce','ce','ce','pe','pe','pe','pe','pe','pe','pe' ],
    # 'oi': [100,150,500,800,450,200,77,50,500,210,300,150,60,17]})
    # chart = alt.Chart(df).mark_bar().encode(
    # x='strike:N',
    # y='oi:Q',
    # color='opttype:N',
    # column='opttype:N').properties(width=300)
    # return chart


    # df = pd.DataFrame({
    # 'x': [1, 2, 3, 4, 5, 1, 2, 9, 4, 5],
    # 'y': [2, -1, 5, -3, -1, 1, 2, 3, 4, 5]})
    # chart = alt.Chart(df).mark_bar().encode(
    # x=alt.X("x:O", scale=alt.Scale(domain=[0, 10])),
    # y=alt.Y("y:Q", scale=alt.Scale(domain=[-8, 8]),)).properties(width=1000, height=400)

    # df = pd.DataFrame({
    # 'x': [1, 2, 3, 4, 5],
    # 'y': [2, -1, 5, -3, -1]})
    # chart = alt.Chart(df).mark_bar().encode(
    # x='x:O',
    # y='y:Q').properties(width=800, height=400)

    # return chart

    








    # df = pd.DataFrame({
    # "Reddit Rating": [1, 2, 3, 4, 5, 1, 2, 9, 4, 5],
    # "Twitter Ranking": [2, -1, 5, -3, -1, 1, 2, 3, 4, 5],
    # "Reddit Likes": [1, 2, 3, 4, 5, 1, 20, 9, 4, 5],
    # "Twitter Likes": [10, 2, 3, 4, 5, 1, 2, 9, 4, 5],})
    # chart = alt.Chart(df).mark_circle().encode(
    # x="Reddit Rating",
    # y="Twitter Ranking",
    # color = "Twitter Likes",
    # size = "Reddit Likes")

    # return chart


# def reddit_top_comments():
#     reddit_top_three_comments = """
#         select * from (select title, comment, upvotes,rank() over(partition by title order by upvotes desc) rank
#         from reddit_comments 
#         order by title, rank) p
#         where rank <= 3;
#     """
























