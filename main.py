"""
This program is to combine concepts tested in other programs.
Description: Program compairs two low quality images for differences.  If the differences is beyond the peramiter I set (normally 0.3)
the program willl take another picture (this time high quality) and upload all three images to twitter
file name:all.py
date: june 8th 2016
my name: william
"""

import picamera
import time
from PIL import Image
from itertools import izip
import twython
from twython import Twython

camera = picamera.PiCamera()
cutoff = 0.2 #0.3 in class room 0.2 in bedroom

#camera.vflip = True #coment out if camera will be upright
camera.brightness = 75 #best at 75
camera.exposure_mode = "off"#off,auto,night,backlight,fireworks (I think the best mode if "off" in this instance\
camera.resolution = (100,100)

key = "API KEY GOES HERE" #my api key
secret = "SECRET KEY GOES HERE"
token = "TOKEN GOES HERE"#the vars used to link program to account
secretToken = "SECRET TOKEN GOES HER"
api = Twython(key,secret,token,secretToken) #uses vars to connect to my account
tweetStr = "update:"

running = True

while running is True:
    camera.capture('1.png')
    img = Image.open('1.png').convert('LA')
    img.save('1.png')#block takes first picture and makes it black and white
    print "image 1 has been taken"

    camera.capture('2.png')
    img2 = Image.open('2.png').convert('LA')
    img2.save('2.png')#block takes 2nd picture and makes it black and white
    print "image 2 has been taken"

    i1 = Image.open("1.png")#block gets images so thjey can be used
    i2 = Image.open("2.png")

    pairs = izip(i1.getdata(), i2.getdata())#gets information about the image
    if len(i1.getbands()) == 1:#gets the "mode" of an image (1 means monochrome)
        dif = sum(abs(p1-p2) for p1,p2 in pairs)#calculates difference if monochrome
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))#calculates difference if not monochrome

    ncomponents = i1.size[0] * i1.size[1] *3
    final = (dif / 255.0 * 100)/ ncomponents
    print "difference (precentage):", final
    

    if (final > cutoff):
        camera.resolution = (1000,600)
        camera.brightness = 50
        camera.exposure_mode = "auto"
        camera.capture('image.jpg')
        
        image = open('image.jpg')# gets my photo
        image2 = open('2.png')
        image3 = open('1.png')
        
        responce = api.upload_media(media=image)#var used to say use this photo
        responce2 = api.upload_media(media=image2)
        responce3 = api.upload_media(media=image3)
        
        api.update_status(status=tweetStr, media_ids=[responce['media_id'],responce2['media_id'],responce3['media_id']])
       
        print "photo has launched!"
        camera.exposure_mode = "off"
        camera.resolution = (100,100)
        camera.brightness = 75
