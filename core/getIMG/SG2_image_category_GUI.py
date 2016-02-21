from kivy.app import App
from kivy.uix.button import Button
import numpy as np
from kivy.core.image import Image as CoreImage

img_dir = '/Users/jingluo/Research_codes/sg2/getIMG'

class category_image(App):
    def build(self):

    def get_image(self):
        Image(source=img_dir + 'STS113-E-5470.jpg')
