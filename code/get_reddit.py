import os

from dotenv import load_dotenv
import praw
import datetime

load_dotenv()

client_id=os.environ["CLIENT_ID"]
client_secret=os.environ["CLIENT_SECRET"]
user_agent=os.environ["USER_AGENT"]
password=os.environ["PASSWORD"]
username=os.environ["USERNAME"]

reddit = praw.Reddit(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    user_agent=os.environ["USER_AGENT"],
    password=os.environ["PASSWORD"],
    username=os.environ["USERNAME"]
)

### RUN THE PRINT STATEMENT BELOW TO OBTAIN AUTHORIZATION URL
### returns a URL. paste into browser and click "accept" to gain access
#print(reddit.auth.url(scopes=["identity"], state="...", duration="permanent"))

### IF ACCESS IS GRANTED SUCCESSFULLY, THE FOLLOWING PRINT STATEMENTS RETURNS REFRESH TOKEN
#print(reddit.auth.authorize(code))
#print(reddit.user.me())

def scrape_posts(n):
    """
    Scrapes the top n number of monthly posts from the politics subreddit page.
    Returns a list of lists that includes:
    [post_id, title, url, # upvotes, # comments, datetime object of posting]
    """
    top_posts = reddit.subreddit('Politics').top(time_filter = 'month', limit=n)
    output = []
    for post in top_posts:
        output.append([post.id, post.title, post.url, post.score, post.num_comments, datetime.datetime.fromtimestamp(post.created)])

    return output



def scrape_comments(input):
    """
    Scrapes the comments from each post.
    Returns a list of lists for top-level comments that includes:
    [post_id, post_title, comment, # upvotes]
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
                output.append([row[0], row[1], comment.replace('\n', ' '), top_level_comment.ups])
    return output
