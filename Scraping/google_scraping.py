import datetime
import re
from bs4 import BeautifulSoup
import requests
import urllib.request
import urllib.parse
import shutil
import os

def Times():
    name = str(datetime.datetime.now())
    name = re.sub('[-:. ]','', name) + '.jpg'
    return name


def Image(search):
    # make the folder to save image
    try:
        if not(os.path.isdir(search)):
            os.makedirs(os.path.join(search))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise
    # move the img 'src' to 'des'
    src = '/home/jj/py/img/'
    des = '/home/jj/py/img/' + search + '/'
    # google search url
    searchUrl = "https://www.google.co.kr/search?q="+search+"&newwindow=1&safe=off&dcr=0&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjC_5L0y4HaAhXIy7wKHamZA2gQ_AUICigB&biw=1920&bih=949"

    req = urllib.request.Request(searchUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'})

    with urllib.request.urlopen(req) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all(class_="rg_ic rg_i")
    print("download start")
    for i in range(0, len(data)):
        if "src" in str(data[i]) :
            imgUrl = (str(data[i]).split('src=\"')[1].split('\"')[0])
            name = Times()
            urllib.request.urlretrieve(imgUrl, name)
            shutil.move(src + name, des + name)
    print("download finish")

keyword = str(input("input the keyword: "))
keyword = re.sub('[ ]','+', keyword)
print(keyword)
Image(keyword)
