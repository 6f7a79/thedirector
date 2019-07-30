import thedirector.modules.tgmessage as tgMessage
import thedirector.modules.tgcallback as tgCallback
import thedirector.modules.tgchannel as tgChannel
import thedirector.modules.tginline as tgInline
from thedirector.modules.misc import Misc
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from threading import Thread
import sqlite3


class cyBot:
    allowed_chats = [-1001218498698, -1001171687704, -1001183412743, -1001159342300, -1001348779356, -1001080335523]
    # allowed_chats = []
    allowed_channels = [-1001183412743, -1001308153582, -1001428687999, -1001410198217, -1001446957910, -1001257020477]
    mimetypes = ["application/pdf", "application/epub+zip", "application/x-mobipocket-ebook", "application/msword", "application/x-bittorrent", "text/plain", "application/x-rar-compressed", "application/zip", "application/x-7z-compressed"]
    log_channel = "-1001183412743"
    file_channel = "@cyfiles"
    replytomessage = False

    def __init__(self, bot, update):
        if update:
            self.bot = bot
            self.update = update
            try:
                self.chat_id = self.update.message.chat.id
                self.message_id = self.update.message.message_id
            except AttributeError:
                pass
        else:
            return

        if self.update.message:

            if self.update.message.document:
                file_id = self.update.message.document.file_id
                file_name = self.update.message.document.file_name
                file_size = self.update.message.document.file_size
                file_mimetype = self.update.message.document.mime_type
                file_by = self.update.message.from_user.id

                # make backup of file
                if file_mimetype in self.mimetypes:
                    file_data = "`{id}` -- *{name}*\n_{size}_ | {mimetype}\n\nby: `#id{uid}`".format(id=file_id, name=file_name, size=file_size, mimetype=file_mimetype, uid=file_by)
                    conn = sqlite3.connect('cyfiles.db')
                    db = conn.cursor()

                    try:
                        db.execute('insert into files values ("", ?, ?, ?, ?, ?)', (file_id, file_name, file_size, file_mimetype, file_by))
                        conn.commit()
                        self.bot.sendDocument(chat_id=self.file_channel, caption=file_data, parse_mode="Markdown", document=file_id, disable_notification=1)
                        conn.close()
                    except sqlite3.IntegrityError:
                        conn.close()
                        return

            elif self.update.message.new_chat_members and self.update.message.chat.id in self.allowed_chats:
                for member in self.update.message.new_chat_members:
                    if Misc().isArabic(member.first_name):
                        self.bot.kickChatMember(chat_id=self.chat_id, user_id=member.id)
                        self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="HTML", text="<b>[ban]</b>  <i>allahu akabur!1!</i>")
                        return
                    fname = member.first_name.replace('_', '\_')
                    log_nmember = "{fname}\n`#id{id}`\n\nIn: {ctitle}\n> [{fname}](tg://user?id={id})".format(fname=fname, id=member.id, ctitle=update.message.chat.id)
                    self.bot.restrictChatMember(chat_id=self.chat_id, user_id=member.id, until_date=None, can_send_messages=0, can_send_media_messages=0, can_send_other_messages=0, can_add_web_page_previews=0)

                    self.bot.sendMessage(chat_id=self.log_channel, parse_mode="Markdown", text=log_nmember)
                    captcha = [
                        [
                            InlineKeyboardButton("ClickMe", callback_data=member.id)
                        ]
                    ]

                    reply_markup = InlineKeyboardMarkup(captcha)
                    self.bot.sendMessage(chat_id=self.chat_id, reply_to_message_id=self.message_id, parse_mode="Markdown", text="**welcome user!\n[simple user verification]**", reply_markup=reply_markup)

        if self.update.callback_query:
            tgcll = Thread(tgCallback.TgCallback(self.bot, self.update).callback())
            tgcll.start()

        if self.update.message and self.update.message.text and self.update.message.chat.id in self.allowed_chats:
            tgmsg = Thread(tgMessage.TgMessage(self.bot, self.update).message())
            tgmsg.start()

        if self.update.channel_post and self.update.channel_post.chat.id in self.allowed_channels:
            tgchn = Thread(tgChannel.TgChannel(self.bot, self.update).channel())
            tgchn.start()

        if self.update.inline_query:
            tgIln = Thread(tgInline.TgInline(self.bot, self.update).inline())
            tgIln.start()
