from PIL import Image, ImageFont, ImageDraw
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
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
import moviepy.editor as mpe
from images.utils import empty_dir
from decouple import config

import openai

OPENAI_KEY = config('OPENAI_KEY')
openai.api_key = OPENAI_KEY

from images.utils import add_text_to_image
from decouple import config

image_folder = 'videos/images'
video_name = 'video.avi'

empty_dir(image_folder)

query = 'football'


def gen_img():
    NEWS_KEY = config('NEWS_KEY')

    newsapi = NewsApiClient(api_key=NEWS_KEY)

    end_day = datetime.datetime.now()
    d = datetime.timedelta(days=30)
    start_day = (end_day - d).strftime('%Y-%m-%d')
    end_day = end_day.strftime('%Y-%m-%d')

    filters = dict(
        size='=1080x1920',
        license='commercial,modify')

    all_articles = newsapi.get_everything(q=query,
                                          from_param=start_day,
                                          to=end_day,
                                          language='en',
                                          sort_by='relevancy')
    titles = []
    for a in all_articles['articles'][0:1]:
        title = a['title']
        print(a['description'])
        titles.append(title)
        # print(title)
        google_Crawler = GoogleImageCrawler(
            storage={'root_dir': r'videos/images/'})
        google_Crawler.crawl(keyword=query, max_num=10)


gen_img()
images = []
img_clips = []
path_list = []

# maxWidth = float('-inf')
# maxHeight = float('-inf')

for img in os.listdir(image_folder):
    frame = cv2.imread(image_folder + "/" + img)
    height, width, layers = frame.shape
    if img.endswith(".jpg"):
        path_list.append(os.path.join(image_folder, img))

for img_path in path_list:
    slide = ImageClip(img_path, duration=2)
    img_clips.append(slide)

video_slides = concatenate_videoclips(img_clips, method='compose')
video_slides.write_videofile("output_video.mp4", fps=24)

#
# frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape
#
# video = cv2.VideoWriter(video_name, 0, 1, (1080, 1920))
#
# for image in images:
#     video.write(cv2.imread(os.path.join(image_folder, image)))
#
# cv2.destroyAllWindows()
# video.release()
#
# # The text that you want to convert to audio

prompt = "Generate a video script {}".format(query)
video_script = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)["choices"][0]["text"]

language = 'en'

myobj = gTTS(text=video_script, lang=language, slow=False)

myobj.save("sound/welcome.mp3")

# os.system("start welcome.mp3")
#
my_clip = mpe.VideoFileClip('video.avi')
audio_background = mpe.AudioFileClip('welcome.mp3')
final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(final_audio)
