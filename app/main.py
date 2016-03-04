from forum import ForumPosts
from slack import Slack


if __name__ == '__main__':

    posts = ForumPosts()
    uncommented_posts = posts.filter_uncommented_posts()

    for post in uncommented_posts:
        slack = Slack(post.slack_text.asdict())
        slack.post()
