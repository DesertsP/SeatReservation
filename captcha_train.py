import requests
from PIL import Image
from StringIO import StringIO
import hashlib
import time


CAPTCHA_URL = "http://202.206.242.87/simpleCaptcha/captcha"


def getImg():
    img_res = requests.get(CAPTCHA_URL)
    img = Image.open(StringIO(img_res.content))
    img = img.convert("P")
    im2 = Image.new("P", img.size, 255)

    for x in range(img.size[1]):
        for y in range(img.size[0]):
            pix = img.getpixel((y, x))
            if pix in range(0, 90):
                im2.putpixel((y, x), 0)
    im2.show()
    return im2


def separate():
    img = getImg()
    inletter = False
    foundletter = False
    start = 0
    end = 0
    letters = []
    for y in range(img.size[0]):
        for x in range(img.size[1]):
            pix = img.getpixel((y, x))
            if pix != 255:
                inletter = True
        if foundletter is False and inletter is True:
            foundletter = True
            start = y
        if foundletter is True and inletter is False:
            foundletter = False
            end = y
            letters.append((start, end))
        inletter = False
    count = 0
    for letter in letters:
        m = hashlib.md5()
        im3 = img.crop((letter[0], 0, letter[1], img.size[1]))
        m.update("%s%s" % (time.time(), count))
        im3.save("./%s.gif" % (m.hexdigest()))
        count += 1

    print letters
    return letters

# for x in range(100):
    # separate()
