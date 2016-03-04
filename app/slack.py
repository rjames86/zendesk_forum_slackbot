from bs4 import BeautifulSoup
import json
import requests


from config import (
    SLACKBOT_URL,
    SLACKBOT_USERNAME,
    SLACKBOT_CHANNEL,
)


class Slack(object):
    def __init__(self, shout):
        self.shout = shout

    def post(self):
        requests.post(
            SLACKBOT_URL,
            data=json.dumps(self.generate_data()),
        )

    def generate_data(self):
        '''
        This could probably be better to support all the
        arguments that Slack could expect
        '''
        data = {
            'username': SLACKBOT_USERNAME,
            'channel': SLACKBOT_CHANNEL,
            'attachments': [
                dict(
                    text=self.shout.get('text'),
                    pretext=self.shout.get('pretext'),
                    author_name=self.shout.get('author_name'),
                    author_link=self.shout.get('author_link'),
                    author_icon=self.shout.get('author_icon'),
                    )]
            }
        return data


class SlackText(object):
    def __init__(self, post):
        self.post = post

    @property
    def pretext(self):
        if self.post.is_old_and_uncommented():
            return "This post is over %s hours old and uncommented" % (self.post.post_age.seconds / 60 / 60)
        return "There are %s comments" % self.comment_count

    @property
    def text(self):
        soup = BeautifulSoup(self.post.details, "html.parser")
        text = soup.getText()
        return text

    def asdict(self):
        '''
        This dictionary should map to the parameters that Slack
        expects in the attachments.
        '''
        return dict(
            pretext=self.pretext,
            text=self.text,
            author_name=self.post.title,
            author_link=self.post.html_url
        )
