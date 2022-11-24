from PIL import Image
import numpy as np

def cropCenter(img,new_width,new_height):

    im = img
    width, height = im.size   

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    crop_im = im.crop((left, top, right, bottom)) #Cropping Image 

    return crop_im