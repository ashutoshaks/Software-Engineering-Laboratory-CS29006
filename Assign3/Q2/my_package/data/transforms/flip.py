#Imports
from PIL import Image, ImageOps

class FlipImage(object):
    '''
        Flips the image.
    '''

    def __init__(self, flip_type = 'horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''
        self.flip_type = flip_type

        
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        if(self.flip_type == "horizontal"):
            flipped_image = ImageOps.mirror(image)
        else:
            flipped_image = ImageOps.flip(image)
        return flipped_image
