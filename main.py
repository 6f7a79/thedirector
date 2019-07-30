from time import sleep
import telegram
from telegram.error import NetworkError, Unauthorized
from threading import Thread
import thedirector.modules.cybot


update_id = None
token = ""


class main():

    def runBot(self, bot):
        self.bot = bot
        try:
            update_id = self.bot.getUpdates()[0]['update_id']
        except IndexError:
            update_id = None

        print("last update_id {}".format(update_id))
        sleep(1)
        while True:
            try:
                for update in self.bot.getUpdates(offset=update_id, timeout=4):
                    print("update > {}".format(update))
                    update_id = update.update_id + 1
                    thBot = Thread(target=thedirector.modules.cybot.cyBot, args=[bot, update])
                    thBot.start()
                    sleep(0.4)
            except NetworkError:
                sleep(1)
            except Unauthorized:
                update_id += 1
            except Exception:
                pass


if __name__ == '__main__':
    bot = main()
    btobj = telegram.Bot(token)
    bot.runBot(btobj)
