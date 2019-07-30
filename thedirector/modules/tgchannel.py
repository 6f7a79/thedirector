from thedirector.modules.tgupdate import TgUpdate
import thedirector.modules.misc as miscellaneous
from thedirector.modules.utils import socialNet


class TgChannel(TgUpdate):
    def __init__(self, bot, update):
        self.misc = self.misc = miscellaneous.Misc()
        TgUpdate.__init__(self, bot, update)

    def channel(self):
        snet = socialNet()

        if self.update.channel_post.entities:
            self.post = self.misc.parserEntities(self.update.channel_post.entities, self.update.channel_post.text)
            if not self.post:
                return

            snet.rdSubmit(self.post)
            snet.twPost(self.post)
