from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import datetime
from datetime import date
from icrawler.builtin import GoogleImageCrawler
from matplotlib import pyplot as plt
import os, shutil
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

def empty_dir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def process_img(titles):
    for i in range(0, len(os.listdir(base_path))):
        infolder = os.listdir(base_path)[i]
        print("folder : " + infolder)
        name = infolder.split('.')[0]
        print(base_path + infolder)
        for infile in os.listdir(base_path + infolder):
            print(infile)
            img = cv2.imread(base_path + infolder + "/" + infile)

            height, width, channels = img.shape
            pos = (10, int(height * 0.70))
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

            cv2.imshow("img", image)
            cv2.waitKey(0)
            print("Do you want to save the image?")
            response = str(input())
            if response == "yes":
                cv2.imwrite(new_path + str(i) + "_out.jpg", image)


print("Starting...")

newsapi = NewsApiClient(api_key=NEWS_KEY)
empty_dir(base_path)
empty_dir(new_path)
# print("Query:")
# domain = str(input())
# print("Number of days:")
# days = int(input())
# print("Number of images:")
# nr_img = int(input())
# print("Number of articles:")
# nr_art = int(input())

domain = "world cup"
days = 5
nr_img = 3
nr_art = 1

end_day = datetime.datetime.now()
d = datetime.timedelta(days=30)
start_day = (end_day - d).strftime('%Y-%m-%d')
end_day = end_day.strftime('%Y-%m-%d')

all_articles = newsapi.get_everything(q=domain,
                                      from_param=start_day,
                                      to=end_day,
                                      language='en',
                                      sort_by='relevancy')
titles = []
for a in all_articles['articles'][0:nr_art]:
    title = a['title'].replace("’", "'")
    titles.append(title)
    google_Crawler = GoogleImageCrawler(
        storage={'root_dir': r'images/raw/' + str(len(titles))})
    filters = dict(
        size='medium')
    google_Crawler.crawl(keyword=title, max_num=nr_img, filters=filters)

print(titles)
process_img(titles)
