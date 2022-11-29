from PIL import Image, ImageFont, ImageDraw
from newsapi import NewsApiClient
import datetime
from datetime import date
from icrawler.builtin import GoogleImageCrawler
from matplotlib import pyplot as plt
import os
import cv2

base_path = "./images/raw/"
new_path = "./images/new/"

def write_img(name, arr):
    cv2.imwrite(new_path + name + '.jpg', arr, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

print("Starting...")

newsapi = NewsApiClient(api_key='')

end_day = datetime.datetime.now()
d = datetime.timedelta(days=2)
start_day = (end_day - d).strftime('%Y-%m-%d')
end_day = end_day.strftime('%Y-%m-%d')

all_articles = newsapi.get_everything(q='Esports',
                                      from_param=start_day,
                                      to=end_day,
                                      language='en',
                                      sort_by='popularity')
titles = []
for a in all_articles['articles'][0:5]:
    title = a['title']
    titles.append(title)
    # print(title)
    # google_Crawler = GoogleImageCrawler(
    #     storage={'root_dir': r'images/raw/'+str(len(titles))})
    # google_Crawler.crawl(keyword=title, max_num=1)

for i in range(0, len(os.listdir(base_path))):
    infile = os.listdir(base_path)[i]
    print("file : " + infile)
    name = infile.split('.')[0]
    img = cv2.imread(base_path + infile)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 500)
    fontScale = 1
    fontColor = (255, 255, 255)
    thickness = 1
    lineType = 2
    print(titles)
    cv2.putText(img, titles[i],
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    cv2.imshow("img", img)
    cv2.imwrite("out.jpg", img)
    cv2.waitKey(0)