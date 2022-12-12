from instabot import Bot

bot = Bot()

bot.login(username="user_name",
          password="user_password")

bot.upload_photo("Technical-Scripter-2019.jpg",
                 caption="Technical Scripter Event 2019")