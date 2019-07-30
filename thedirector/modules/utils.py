from praw import Reddit
from twitter import Api

reddit = Reddit(client_id='',
                client_secret='',
                password='',
                user_agent='',
                username='')
twitter = Api(consumer_key='',
              consumer_secret='',
              access_token_key='',
              access_token_secret='')


class Utils:
    def __init__(self, bot, chat_id, message_id):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id

    def replyMsg(self, text, parse_mode="Markdown", reply_markup=None):
        self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)


class socialNet():
    global reddit, twitter

    def twPost(self, content):
        hashtag = ''

        if not len(content["hashtags"]) >= 1:
            for ht in content["hashtags"]:
                hashtag += ht + " "
        else:
            hashtag = ''

        tweet = "{} {} {}".format(hashtag, content["title"], content["url"])
        twitter.PostUpdate(tweet)

    def rdSubmit(self, post):
        reddit.subreddit("cryptobrasil").submit(post["title"], url=post["url"])
        # print("\n\t{}".format(originalrd))
        # crs = reddit.submission(id=originalrd)
        # crs.crosspost(subreddit="cryptobrasil", send_replies=False)
        # sleep(6)
        # reddit.subreddit("cryptobrasil").submit(post["title"], url=post["url"])
