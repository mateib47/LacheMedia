from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import datetime
from datetime import date
from icrawler.builtin import GoogleImageCrawler
from matplotlib import pyplot as plt
import os
import cv2
import numpy as np
from typing import Optional, Tuple
import importlib
from gtts import gTTS


from images.utils import add_text_to_image
from decouple import config

image_folder = 'videos/images'
video_name = 'video.avi'

def gen_img():
    NEWS_KEY = config('NEWS_KEY')

    newsapi = NewsApiClient(api_key=NEWS_KEY)

    end_day = datetime.datetime.now()
    d = datetime.timedelta(days=30)
    start_day = (end_day - d).strftime('%Y-%m-%d')
    end_day = end_day.strftime('%Y-%m-%d')

    all_articles = newsapi.get_everything(q='KO Izzy UFC',
                                          from_param=start_day,
                                          to=end_day,
                                          language='en',
                                          sort_by='relevancy')
    titles = []
    for a in all_articles['articles'][0:1]:
        title = a['title']
        titles.append(title)
        # print(title)
        google_Crawler = GoogleImageCrawler(
            storage={'root_dir': r'videos/images/'})
        google_Crawler.crawl(keyword=title, max_num=20)

gen_img()
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
#
# # The text that you want to convert to audio
# mytext = 'Bine ati venit la LacheMedia!'
#
# language = 'ro'
#
# myobj = gTTS(text=mytext, lang=language, slow=False)
#
# myobj.save("sound/welcome.mp3")
#
# os.system("start welcome.mp3")
