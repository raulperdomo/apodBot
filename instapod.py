#!/usr/bin/python

from PIL import Image
import requests
from lxml import html
import urllib
from InstagramAPI import InstagramAPI

apod = requests.get('http://apod.nasa.gov/')
et = html.fromstring(apod.text)
image = et.xpath('/html/body/center[1]/p[2]/a')
imagePath = image.pop().attrib['href']
apodPath = "http://apod.nasa.gov/"+imagePath
print(apodPath)
hiRes = urllib.request.urlretrieve(apodPath,'./apod.jpg')
img = Image.open('./apod.jpg')
if img.size[0] > img.size[1]:
    longer_side = max(img.size)
    horizontal_padding = (longer_side - img.size[0]) / 2
    vertical_padding = (longer_side - img.size[1]) / 2
    imgNew = img.crop(
        (
        -horizontal_padding,
        -vertical_padding,
        img.size[0] + horizontal_padding,
        img.size[1] + vertical_padding
        )
    )
imgNew.save("./apodPadded.jpg")
explanation = et.xpath('/html/body/p[1]')
ex2 = et.xpath('/html/body/p[1]/text()')
ex2.reverse()
description = ''
for child in explanation[0].iter():
    description = description + " "+child.text.strip()   
    description = description + " "+ex2.pop().strip()
description = description+" #nasa #space #esa #apod #astronomy #astrophotography"
try:
    InstagramAPI = InstagramAPI("username", "password")
    InstagramAPI.login()  # login
    photo_path = './apodPadded.jpg'
    InstagramAPI.uploadPhoto(photo_path, caption=description)
except:
    print("Could not post to Instagram")
