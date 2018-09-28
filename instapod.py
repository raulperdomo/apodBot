#!/usr/bin/python

from PIL import Image
import requests
from lxml import html
import urllib
import sys
from InstagramAPI import InstagramAPI

apod = requests.get('http://apod.nasa.gov')
et = html.fromstring(apod.text)
image = et.xpath('/html/body/center[1]/p[2]/a')
imagePath = image.pop().attrib['href']
apodPath = "http://apod.nasa.gov/"+imagePath
print(apodPath)
urllib.request.urlretrieve(apodPath,'./apod.jpg')
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
    
else:
    img.save("./apodPadded.jpg")

explanation = et.xpath('/html/body/p[1]')[0]
description = ' '.join(explanation.text_content().split())
description = description + '\n#nasa #space #esa #apod #astronomy #astrophotography\n'
credit = et.xpath('/html/body/center[2]/a')[0].text_content()
creditString = '📷: '+ ' '.join(credit.split())
title = et.xpath('/html/body/center[2]/b[1]')[0].text.strip() + '\n'
description = title + description + creditString
print(description)
try:
	InstagramAPI = InstagramAPI("username", "password")
	InstagramAPI.login()  # login
	photo_path = './apodPadded.jpg'
	InstagramAPI.uploadPhoto(photo_path, caption=description)
except:
	print("Could not post to Instagram" + str(sys.exc_info()[0]))


