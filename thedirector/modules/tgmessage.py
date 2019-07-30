import thedirector.modules.utils as util
import thedirector.modules.misc as miscellaneous
from thedirector.modules.tgupdate import TgUpdate
import telegram


class TgMessage(TgUpdate):
    def __init__(self, bot, update):
        self.misc = miscellaneous.Misc()
        TgUpdate.__init__(self, bot, update)

    def checkIsReply(self):
        if self.update.message.reply_to_message:
            self.replytomessage = True
            self.target_user_id = self.update.message.reply_to_message.from_user.id
            self.target_message_id = self.update.message.reply_to_message.message_id
            self.target_fname = self.update.message.reply_to_message.from_user.first_name
            self.target_username = self.update.message.reply_to_message.from_user.username

    def message(self):
        self.checkIsReply()
        self.chat_id = self.update.message.chat.id
        self.message_id = self.update.message.message_id
        backup_channel = "@pr1v8_board"
        admin_list = self.bot.getChatAdministrators(chat_id=self.chat_id)
        user_id = self.update.message.from_user.id
        user_fname = self.update.message.from_user.first_name
        sudo = self.misc.isAdm(user_id=user_id, admin_list=admin_list)
        txt = self.update.message.text.split(" ")
        command = txt[0]
        remain_txt = ' '.join(txt[1:])
        query = True
        utils = util.Utils(self.bot, self.chat_id, self.message_id)

        if not remain_txt:
            remain_txt = "-"
            query = False

        if command == "/sudo" and sudo:
            utils.replyMsg(text="hello root")
        elif command == "/free" and self.replytomessage and sudo:
            self.bot.restrictChatMember(chat_id=self.chat_id, user_id=self.target_user_id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
            utils.replyMsg(text="user unmuted")
        elif command == "/link":
            link = self.bot.exportChatInviteLink(chat_id=self.chat_id)
            utils.replyMsg(text=link)
        elif command == "/afk" or command == "/off":
            afk = "*user* [{fname}](tg://user?id={id}) *is afk*\n    *> {reason}*".format(fname=user_fname, id=user_id, reason=remain_txt)
            utils.replyMsg(text=afk)
        elif command == "/back" or command == "/on":
            back = "*user* [{fname}](tg://user?id={id}) *is back*\n    *> {reason}".format(fname=user_fname, id=user_id, reason=remain_txt)
            utils.replyMsg(text=back)
        elif command == "/ban" and self.replytomessage and sudo:
            ban = "*user* [{fname}](tg://user?id={id}) *banned*".format(fname=self.target_fname, id=self.target_user_id)
            self.bot.kickChatMember(chat_id=self.chat_id, user_id=self.target_user_id)
            utils.replyMsg(text=ban)
        elif command == "/unban" and self.replytomessage and sudo:
            unban = "*user* [{fname}](tg://user?id={id}) *unbanned*".format(fname=self.target_fname, id=self.target_user_id)
            self.bot.unbanChatMember(chat_id=self.chat_id, user_id=self.target_user_id)
            utils.replyMsg(text=unban)
        elif command == "/mute" and self.replytomessage and sudo:
            mute = "*user* [{fname}](tg://user?id={id}) *muted*".format(fname=self.target_fname, id=self.target_user_id)
            self.bot.restrictChatMember(chat_id=self.chat_id, user_id=self.target_user_id, until_date=None, can_send_messages=0, can_send_media_messages=0, can_send_other_messages=0, can_add_web_page_previews=0)
            utils.replyMsg(text=mute)
        elif command == "/unmute" and self.replytomessage and sudo:
            unmute = "*user* [{fname}](tg://user?id={id}) *unmuted*".format(fname=self.target_fname, id=self.target_user_id)
            self.bot.restrictChatMember(chat_id=self.chat_id, user_id=self.target_user_id, until_date=None, can_send_messages=1, can_send_media_messages=1, can_send_other_messages=1, can_add_web_page_previews=1)
            utils.replyMsg(text=unmute)
        elif command == "/pin" and self.replytomessage and sudo:
            self.bot.pinChatMessage(chat_id=self.chat_id, message_id=self.target_message_id, disable_notification=1)
            utils.replyMsg(text="*message pinned*")
        elif command == "/uinfo" and self.replytomessage and sudo:
            uinfo = "*user info* | [{fname}](tg://user?id={id})\nname: {fname}\nid: `#id{id}`\nusername: @{username}".format(fname=self.target_fname, id=self.target_user_id, username=self.target_username)
            utils.replyMsg(text=uinfo)
        elif command == "/ginfo":
            gmember = self.bot.getChatMembersCount(chat_id=self.chat_id)
            ginfo = "*group info* | [{title}](tg://chat?id={id})\nTitle: {title}\nid: `{id}`\nMembers: {count}".format(title=self.update.message.chat.title, id=self.chat_id, count=gmember)
            utils.replyMsg(text=ginfo)
        elif command == "/getfile" and sudo and query:
            self.bot.sendDocument(chat_id=self.chat_id, reply_to_message_id=self.message_id, document=remain_txt)
        elif command == "/save" and self.replytomessage and sudo:
            self.bot.forwardMessage(chat_id=backup_channel, from_chat_id=self.chat_id, message_id=self.target_message_id)
        elif command == "/rtfm":
            utils.replyMsg(text="**read the fucking manual**\nhttps://en.wikipedia.org/wiki/RTFM")
        elif command == "/w":
            captcha = [
                [
                    telegram.InlineKeyboardButton("me", callback_data='w')
                ]
            ]
            reply_markup = telegram.InlineKeyboardMarkup(captcha)
            utils.replyMsg(text="**Who is online?**", reply_markup=reply_markup)
        elif command == "/popup":
            botao = remain_txt.split('<>')[0]
            captcha = [
                [
                    telegram.InlineKeyboardButton(botao, callback_data="popup")
                ]
            ]
            reply_markup = telegram.InlineKeyboardMarkup(captcha)
            self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, text="some popup texts", parse_mode="Markdown", reply_markup=reply_markup)
