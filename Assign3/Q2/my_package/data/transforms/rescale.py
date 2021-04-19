#Imports


class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size):
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
        '''
        self.output_size = output_size

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        # if output_size is int, smaller of image edges is matched to output_size keeping aspect ratio the same
        if(isinstance(self.output_size, int)):
            if(image.size[0] < image.size[1]):
                w = self.output_size
                h = int(image.size[1] * (w / image.size[0]))
            else:
                h = self.output_size
                w = int(image.size[0] * (h / image.size[1]))

        # if output_size is float, then output_size is taken as the aspect ratio
        elif(isinstance(self.output_size, float)):
            w = int(image.size[0] * self.output_size)
            h = int(image.size[1] * self.output_size)

        # otherwise if output_size is a tuple, that is the desired output size
        else:
            w, h = self.output_size

        rescaled_image = image.resize((w, h))
        return rescaled_image

