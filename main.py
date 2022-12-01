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

from images.utils import add_text_to_image
from decouple import config

NEWS_KEY = config('NEWS_KEY')

base_path = "./images/raw/"
new_path = "./images/new/"


def write_img(name, arr):
    cv2.imwrite(new_path + name + '.jpg', arr, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


def draw_text(img, text,
              font=cv2.FONT_HERSHEY_PLAIN,
              pos=(10, 400),
              font_scale=3,
              font_thickness=2,
              text_color=(0, 255, 0),
              text_color_bg=(0, 0, 0)
              ):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size


print("Starting...")

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
for a in all_articles['articles'][0:5]:
    title = a['title']
    titles.append(title)
    # print(title)
    google_Crawler = GoogleImageCrawler(
        storage={'root_dir': r'images/raw/' + str(len(titles))})
    google_Crawler.crawl(keyword=title, max_num=1)

for i in range(0, len(os.listdir(base_path))):
    infile = os.listdir(base_path)[i]
    print("file : " + infile)
    name = infile.split('.')[0]
    print(base_path + infile)
    img = cv2.imread(base_path + infile + '/000001.jpg')

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 500)
    fontScale = 1
    fontColor = (255, 255, 255)
    thickness = 5
    lineType = 2
    print(titles)

    height, width, channels = img.shape
    pos = (10, int(height * 0.70))
    # w, h = draw_text(img, titles[i], pos=pos)
    # draw_text(img, 'LacheMedia', font_scale=4, pos=(0, 20 + h), text_color_bg=(255, 0, 0))

    add_text_to_image(
        img,
        titles[i],
        font_color_rgb=(1, 32, 48),
        top_left_xy=pos,
        bg_color_rgb=(48, 165, 191),
        line_spacing=1.5,
    )
    image = add_text_to_image(
        img,
        'LacheMedia',
        font_color_rgb=(0, 255, 255),
        outline_color_rgb=(255, 0, 0),
        top_left_xy=(10, 10),
        line_spacing=1.5,
        font_face=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    )

    cv2.imshow("img", img)
    cv2.imwrite(new_path+str(i)+"out.jpg", img)
    cv2.waitKey(0)
