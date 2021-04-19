#Imports
from PIL import Image
import random

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type = 'center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''
        self.crop_height = shape[0]
        self.crop_width = shape[1]
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # center crop
        if(self.crop_type == "center"):
            left = (image.size[0] // 2) - (self.crop_width // 2)
            right = left + self.crop_width
            top = (image.size[1] // 2) - (self.crop_height // 2)
            bottom = top + self.crop_height

        # random crop
        else:
            left = random.randrange(0, image.size[0] - self.crop_width)
            right = left + self.crop_width
            top = random.randrange(0, image.size[1] - self.crop_height)
            bottom = top + self.crop_height

        cropped_image = image.crop((left, top, right, bottom))
        return cropped_image