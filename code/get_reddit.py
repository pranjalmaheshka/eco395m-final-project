import os
import csv
from dotenv import load_dotenv
import praw
import pandas as pd
import datetime
from database import engine


load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    user_agent=os.environ["USER_AGENT"],
    password=os.environ["PASSWORD"],
    username=os.environ["USERNAME"]
)

### RUN THE PRINT STATEMENT BELOW TO OBTAIN AUTHORIZATION URL
### returns a URL. paste into browser and click "accept" to gain access
# print(reddit.auth.url(scopes=["identity"], state="...", duration="permanent"))

### IF ACCESS IS GRANTED SUCCESSFULLY, THE FOLLOWING PRINT STATEMENTS RETURNS REFRESH TOKEN
# print(reddit.auth.authorize(code))
# print(reddit.user.me())


def scrape_posts(n):
    """
    Scrapes the top n number of monthly posts from the politics subreddit page.
    Returns a list of lists that includes:
    [post_id, title, url, # upvotes, # comments, datetime object of posting]
    """
    top_posts = reddit.subreddit("Politics").top(time_filter="month", limit=n)
    output = []
    for post in top_posts:
        output.append(
            [
                post.id,
                post.title,
                post.url,
                post.score,
                post.num_comments,
                datetime.datetime.fromtimestamp(post.created),
            ]
        )
    return output


def scrape_posts_dict(n):
    """
    Scrapes the top n number of monthly posts from the politics subreddit page.
    Returns a list of dicts that includes:
    post_id, title, url, # upvotes, # comments, datetime object of posting, news_company, bias_rating
    """
    top_posts = reddit.subreddit("Politics").top(time_filter="month", limit=n)
    output = []
    for post in top_posts:
        url = post.url
        if url[8:12] == "www.":
            index_ = []
            index_count = 0
            for i in url:
                if i == ".":
                    index_.append(index_count)
                index_count += 1
            org_name = url[index_[0] + 1 : index_[1]]
        else:
            index_ = []
            index_count = 0
            for i in url:
                if i == ".":
                    index_.append(index_count)
                index_count += 1
            org_name = url[8 : index_[0]]

        if org_name in ("alternet", "theatlantic", "buzzfeednews", "cnn", "democracynow", "dailybeast", "huffpost", \
            "theintercept", "jacobin", "motherjones", "msnbc", "thenewyorker", "thenation", "slate", "vox", \
            "rollingstone","salon", "newrepublic", "esquire"):
            ratings = 1
        elif org_name in ("abcnews", "apnews", "bloomberg", "cbs", "theguardian", "insider", "nbcnews", "nytimes", "npr", \
            "politico", "propublica", "time", "washingtonpost", "usatoday", "yahoo", "businessinsider", "commondreams", \
            "indpendent"):
            ratings = 2
        elif org_name in ("axios", "bcc", "csmonitor", "forbes", "marketwatch", "newsnation", "newsweek", "reuters", \
            "realclearpolitics", "thehill", "wsj", "cnbc", "abc57", "kentucky"):
            ratings = 3
        elif org_name in ("thedispatch", "theepochtimes", "foxbusiness", "ijr", "nypost", "thepostmillenial", "reason", \
            "washingtonexaminer", "washingtontimes"):
            ratings = 4
        elif org_name in ("theamericanconservative", "spectator", "breitbart", "theblaze", "cbn", "dailycaller", \
            "dailymail", "dailywire", "foxnews", "thefederalist", "nationalreview", "newsmax", "freebeacon", "oann"):
            ratings = 5

        output.append(
            {
                "reddit_post_id": post.id,
                "title": post.title,
                "url": post.url,
                "post_score": post.score,
                "num_comments": post.num_comments,
                "date_posted": datetime.datetime.fromtimestamp(post.created),
                "news_company": org_name,
                "bias_rating": ratings
            }
        )

    return output


def scrape_comments(input):
    """
    Scrapes the comments from each post.
    Returns a list of lists for top-level comments that includes:
    [post_id, post_title, comment, # upvotes, ]
    """
    output = []
    for row in input:
        submission = reddit.submission(id=row[0])
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments.list():
            comment = top_level_comment.body
            if "I am a bot" in comment:
                pass
            else:
                output.append(
                    [
                        row[0],
                        row[1],
                        comment.replace("\n", " "),
                        top_level_comment.ups
                    ]
                )
    return output


def scrape_comments_dicts(input):
    """
    Scrapes the comments from each post.
    Returns a list of dicts for top-level comments that includes:
    [post_id, post_title, comment, # upvotes]
    """
    output = []
    for row in input:
        submission = reddit.submission(id=row["reddit_post_id"])
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments.list():
            comment = top_level_comment.body
            if "I am a bot" in comment or "deleted" in comment:
                pass
            else:
                output.append(
                    {
                        "reddit_post_id": row["reddit_post_id"],
                        "title": row["title"],
                        "comment": comment.replace("\n", " "),
                        "upvotes": top_level_comment.ups
                    }
                )
    return output


def write_data_to_csv(input, file_name, headers):
    """Write the data to the csv file."""
    path = os.path.join("artifacts", file_name)
    with open(path, "w+", newline="", encoding="utf-8") as out_file:
        write = csv.writer(out_file)
        write.writerow(headers)
        write.writerows(input)


# post = scrape_posts(20)
# comments = scrape_comments(post)

# write_data_to_csv(post, "reddit_posts_results.csv", ["id","title","url","score","num_comments","datetime_created"])
# write_data_to_csv(comments, "reddit_comments_results.csv", ["id","title","comment","upvotes"])


def create_table():
    create_table_cmd = """
        create table if not exists reddit_posts (
            reddit_post_id varchar primary key,
            title varchar,
            url varchar,
            post_score numeric,
            num_comments numeric,
            date_posted date,
            news_company varchar,
            bias_rating numeric
        );

        create table if not exists reddit_comments (
            id bigserial,
            reddit_post_id varchar,
            title varchar,
            comment varchar,
            upvotes numeric
        )
    """

    with engine.connect() as connection:
        connection.exec_driver_sql(create_table_cmd)


def insert_many_dict_posts(data):
    """
    Takes a list of posts as dicts. Uses a list of dicts as parameters to insert into sqlalchemy
    """

    insert_template = """
        insert into reddit_posts (reddit_post_id, title, url, post_score, num_comments, date_posted, news_company, bias_rating)
        values (%(reddit_post_id)s, %(title)s, %(url)s, %(post_score)s, %(num_comments)s, %(date_posted)s, %(news_company)s, %(bias_rating)s);
    """

    with engine.connect() as connection:
        connection.exec_driver_sql(insert_template, data)


def insert_many_dict_comments(data):
    """
    Takes a list of posts as dicts. Uses a list of dicts as parameters to insert into sqlalchemy
    """

    insert_template = """
        insert into reddit_comments (reddit_post_id, title, comment, upvotes)
        values (%(reddit_post_id)s, %(title)s, %(comment)s, %(upvotes)s)
    """

    with engine.connect() as connection:
        connection.exec_driver_sql(insert_template, data)


def get_reddit_post_results():
    query_template = """
        select * from reddit_posts;
        select * from reddit_comments
    """
    with engine.connect() as connection:
        result = connection.exec_driver_sql(query_template)

        columns = result.keys()
        raw_data = result.all()
        print(columns)
        print(raw_data)

def nlp_columns():
    query_template = """
    ALTER TABLE reddit_comments
    add people varchar,
    add organization varchar,
    add score_pos numeric,
    add score_compound numeric,
    add score numeric;
    """

    with engine.connect() as connection:
        connection.exec_driver_sql(query_template)



if __name__ == "__main__":
    reddit_posts_dicts = scrape_posts_dict(50)
    reddit_comments_dicts = scrape_comments_dicts(reddit_posts_dicts)
    create_table()
    insert_many_dict_posts(reddit_posts_dicts)
    insert_many_dict_comments(reddit_comments_dicts)
    nlp_columns()
    # get_reddit_post_results()
