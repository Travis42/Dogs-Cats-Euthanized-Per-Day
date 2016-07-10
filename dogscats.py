#! python3
# Creation of a tiled mosaic of random dog and cat images that correspond to the # of dogs
# and cats euthanized in Japan per day.  Can be modified to depict any country.
# Sources:
# USA: Of the 3 million cats and dogs euthanized in shelters each year, approximately
# 2.4 million (80%) are healthy and treatable and could have been adopted into
# new homes http://www.humanesociety.org/issues/pet_overpopulation/facts/pet_o
# wnership_statistics.html ​
# Japan: 850 dogs and cats are killed in shelters
# each day. 
# http://www.conoass.or.jp/situation/
# Graph: Orange line shows the number of cats that are killed. Blue line shows dogs.
# Currently, more cats are killed than dogs.​


from PIL import Image
import os
import random
import re
import numpy as np


def GetFiles(directory):
    '''
    Returns a list of all the matching files in the directory
    '''
    result = []
    prior = os.getcwd()
    os.chdir(prior + directory)
    for filename in os.listdir():
        result.append(os.path.abspath(filename))
    os.chdir(prior)
    return result


def resizeImages(directory, listofpics, origW, origH):
    # resize a list of pics so that they're the same, small size.  Returns small dimensions.
    smallwidth = origW // 5
    smallheight = origH // 5
    prior = os.getcwd()
    os.chdir(prior + directory)
    for i in listofpics:
        orig = Image.open(i)
        smallImg = orig.resize((int(smallwidth), int(smallheight)))
        smallImg.save(i)
    os.chdir(prior)
    return smallwidth, smallheight



# select and load images of dogs
# https://pixabay.com/en/photos/?image_type=&cat=&min_width=&min_height=&q=dog+silhouette&order=popular
doglist = GetFiles('/dogs')
# select and load images of cats
catlist = GetFiles('/cats')
firstimage = Image.open(doglist[0])
origW, origH = firstimage.size
# make small versions of uniform size:
smallwidth, smallheight = resizeImages('/dogs', doglist, origW, origH)
resizeImages('/cats', catlist, origW, origH)


# number of animals euthanized per day in Japan, source:
# http://inuneco-partner.com/inuneco-01.html

dogseuthed = 85000 / 365
catseuthed = 200000 / 365
# euthanizedperday = catseuthed + dogseuthed # 780
euthanizedperday = 850  # using an alternate source per my editor in chief
# 42.5% dogs.
weights = [0.425, 0.575]

# create a large image to place these on
rows = round((euthanizedperday * smallheight) / 10)
canvasW, canvasH = (
    (smallwidth * 10) + 2 * smallwidth,             # width
    (rows + 2 * smallwidth)                         # height
)  

canvas = Image.new('RGBA', (canvasW, canvasH))  # , 'white'
canvas.save('canvas.png')


# copy images onto the canvas to show the number of euthanized cats and dogs
# 0 pix to end, step len of cropped image
count = 0
for left in range(smallwidth, canvasW - smallwidth, smallwidth):
    for top in range(smallheight, rows + smallheight, smallheight):
        # thing to copy on.paste(thing being pasted, (where))
        choices = [random.choice(doglist), random.choice(catlist)]
        rnd = np.random.choice(choices, p=weights)
        im = Image.open(rnd)
        canvas.paste(im, (left, top))
        count += 1
canvas.save('tiled.png')

print ('euthanized per day: ' + str(euthanizedperday))
print ('count: ' + str(count))

