from twitter import Twitter
import time
from media import Media
from twitterquot import Quotes

#deploy ke heroku
tw = Twitter()
qt = Quotes()
media = Media()

def start():
    print("Starting program...")
    dms = list()
    while True:
        if len(dms) != 0:
            for i in range(len(dms)):
                message = dms[i]['message']
                # I take sender_id just in case you want to know who's sent the message
                sender_id = dms[i]['sender_id']
                id = dms[i]['id']

                if len(message) != 0 and len(message) < 280:
                    # prikitiw is the keyword
                    # if you want to turn off the case sensitive like: priktiw, Prikitiw, pRiKiTiw
                    # just use lower(message) and check it, but please remove the replace function line
                    if "lol" or"LOL" or "Lol" in message:
                        message = message.replace("https://", "")
                       # message = message.replace("prikitiw", "")
                        if len(message) != 0:
                            if dms[i]['media'] is None:
                                print("DM will be posted")

                                tw.post_tweet(message)
                                tw.delete_dm(id)
                            else:
                                print("DM will be posted with media")
                                print(dms[i]['shorted_media_url'])
                                tw.post_tweet_with_media(message, dms[i]['media'],dms[i]['shorted_media_url'], dms[i]['type'])
                                tw.delete_dm(id)
                        else:
                            print("DM deleted because its empty..")
                            tw.delete_dm(id)
                    elif "quotes" in message:
                        message = message.replace("quotes", "")
                        if "https://" not in message and "http://" not in message:
                            if "--s" in message:
                                message = message.replace("--s", "")
                                screen_name = qt.get_user_screen_name(sender_id)
                                media.download_image()
                                media.process_image(message, screen_name)
                                qt.post_tweet()
                                qt.delete_dm(id)
                            else:
                                media.download_image()
                                media.process_image(message, None)
                                qt.post_tweet()
                                qt.delete_dm(id)
                        else:
                            qt.delete_dm(id)
                    else:
                        print("DM will be deleted because does not contains keyword..")
                        tw.delete_dm(id)

            dms = list()

        else:
            print("Direct message is empty...")
            dms = tw.read_dm()
            if len(dms) == 0 or dms is None:
                time.sleep(10)

if __name__ == "__main__":
    start()