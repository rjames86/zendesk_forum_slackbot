from zendesk import Zendesk
from zendesk_mapping_table import mapping_table

import dateutil.parser
import datetime

from config import (
    FORUM_EMAIL,
    FORUM_DOMAIN,
    FORUM_API_TOKEN,
)

from slack import (
    SlackText
)


forum = Zendesk(FORUM_DOMAIN,
                FORUM_EMAIL,
                FORUM_API_TOKEN,
                use_api_token=True,
                api_version=2)

# We need to update the mapping table since it doesn't currently
# support the Community API
forum.mapping_table.update(mapping_table)


class ForumPost(object):
    AGE_LIMIT = 2 * 60 * 60  # 2 hours

    def __init__(self, post):
        self.post = post

    def __repr__(self):
        return "<ForumPost(%s)>" % self.id

    def __getattr__(self, name):
        if name in self.post:
            return self.post[name]
        elif hasattr(self, name):
            return object.__getattr__(name)
        else:
            # Default behaviour
            raise AttributeError

    @property
    def slack_text(self):
        return SlackText(self)

    @property
    def created(self):
        return dateutil.parser.parse(self.created_at).replace(tzinfo=None)

    @property
    def post_age(self):
        return datetime.datetime.utcnow() - self.created

    def is_old_and_uncommented(self):
        if (self.post_age.seconds > self.AGE_LIMIT) and self.comment_count == 0:
            return True
        return False


class ForumPosts(list):
    def __init__(self):
        # TODO(ryan) This is a dumb way to do this
        # TODO(ryan) Still need to support pagination
        posts = forum.list_all_posts(sort_by="recent_activity")
        self.extend(map(ForumPost, posts['posts']))

    def filter_by_comment_count(self, count=5):
        return self.filter_by(lambda p: p.comment_count > count)

    def filter_by_pinned(self, pinned=False):
        return self.filter_by(lambda p: p.pinned == pinned)

    def filter_uncommented_posts(self):
        return self.filter_by(lambda p: p.is_old_and_uncommented())

    def filter_by(self, comparator):
        return filter(comparator, self)
