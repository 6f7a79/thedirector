from thedirector.modules.tgupdate import TgUpdate
from time import sleep
from telegram import InlineQueryResultCachedDocument
from uuid import uuid4
import sqlite3


class TgInline(TgUpdate):
    def __init__(self, bot, update):
        TgUpdate.__init__(self, bot, update)

    def inline(self):
        qid = self.update.inline_query.id
        conn = sqlite3.connect('cyfiles.db')
        db = conn.cursor()

        if self.update.inline_query.query:
            sleep(0.3)
            value = self.update.inline_query.query
            textquery = []
            for row in db.execute("SELECT hash, name FROM files WHERE name LIKE ? LIMIT 8", ('%'+value+'%',)):
                query = InlineQueryResultCachedDocument(
                    type='document',
                    id=uuid4(),
                    title=row[1],
                    document_file_id=row[0],
                    caption="*{}* - `{}`".format(row[1], row[0]),
                    parse_mode="Markdown"
                )
                textquery.append(query)
            self.bot.answerInlineQuery(inline_query_id=qid, results=textquery)
