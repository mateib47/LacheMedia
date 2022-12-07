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
import ast

from images.utils import add_text_to_image
from images.utils import empty_dir

from decouple import config

import openai


NEWS_KEY = config('NEWS_KEY')
OPENAI_KEY = config('OPENAI_KEY')
openai.api_key = OPENAI_KEY


base_path = "./images/raw/"
new_path = "./images/new/"


def write_img(name, arr):
    cv2.imwrite(new_path + name + '.jpg', arr, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


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
# print("Generation mode(0 - real news / 1 - openai generation):")
# mode = int(input())

domain = "psychology"
days = 5
nr_img = 1
nr_art = 3
mode = 1

end_day = datetime.datetime.now()
d = datetime.timedelta(days=30)
start_day = (end_day - d).strftime('%Y-%m-%d')
end_day = end_day.strftime('%Y-%m-%d')

titles = []
if mode == 0:
    all_articles = newsapi.get_everything(q=domain,
                                          from_param=start_day,
                                          to=end_day,
                                          language='en',
                                          sort_by='relevancy',
                                          page_size=nr_art)
    for a in all_articles['articles'][0:nr_art]:
        title = a['title'].replace("’", "'")
        titles.append(title)
else:
    prompt = "Generate {} news headlines about {} in the format: [\"news1\", \"news2\",...]".format(nr_art,domain)
    print(prompt)
    titles = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )["choices"][0]["text"]
    titles = ast.literal_eval(titles)
    print(titles)

for t in titles:
    google_Crawler = GoogleImageCrawler(
        storage={'root_dir': r'images/raw/' + str(len(titles))})
    filters = dict(
        size='medium')
    google_Crawler.crawl(keyword=t, max_num=nr_img, filters=filters)

print(titles)
process_img(titles)
