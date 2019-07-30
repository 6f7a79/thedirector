from thedirector.modules.tgupdate import TgUpdate


class TgCallback(TgUpdate):
    def __init__(self, bot, update):
        TgUpdate.__init__(self, bot, update)

    def callback(self):
        cid = self.update.callback_query.message.chat.id
        uid = str(self.update.callback_query.from_user.id)

        if self.update.callback_query.data == uid:
            # unmute user that clicks on button
            self.bot.restrictChatMember(chat_id=cid, user_id=self.update.callback_query.from_user.id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
            self.bot.deleteMessage(chat_id=cid, message_id=self.update.callback_query.message.message_id)
            self.bot.sendMessage(chat_id=cid, reply_to_message_id=self.update.callback_query.message.reply_to_message.message_id, parse_mode="HTML", text="user <b>{}</b> liberado".format(self.update.callback_query.from_user.first_name))
        elif self.update.callback_query.data == 'w':
            self.bot.sendMessage(chat_id=cid, reply_to_message_id=self.update.callback_query.message.reply_to_message.message_id, parse_mode="Markdown", text=" {} here!".format(self.update.callback_query.from_user.first_name))
        elif self.update.callback_query.data == "popup":
            if not self.update.callback_query.message.reply_to_message.text.split(' ')[1:]:
                mtxt = "null"
            else:
                mtxt = ' '.join(self.update.callback_query.message.reply_to_message.text.split('<>')[1].split(" ")[1:])
            self.bot.answerCallbackQuery(callback_query_id=self.update.callback_query.id, text=mtxt, show_alert=True)
