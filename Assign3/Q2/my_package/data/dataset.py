#Imports
import os
import jsonlines
import numpy as np
from PIL import Image
from my_package.data.transforms import BlurImage, CropImage, FlipImage, RescaleImage, RotateImage

class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file, transforms = []):
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''

        data_dir = os.path.dirname(annotation_file)
        self.transforms = transforms
        self.img_data = list()
        with jsonlines.open(annotation_file) as reader:
            for line in reader.iter(type = dict, skip_invalid = True):
                curr_path = os.path.join(data_dir, line["img_fn"])
                curr_dict = {"path" : curr_path, "bboxes" : line["bboxes"]}
                self.img_data.append(curr_dict)


    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.img_data)
        

    def __getitem__(self, idx):
        '''
            return the dataset element for the index: "idx"
            Arguments:
                idx: index of the data element.

            Returns: A dictionary with:
                image: image (in the form of a numpy array) (shape: (3, H, W))
                gt_bboxes: N X 5 array where N is the number of bounding boxes, each 
                            consisting of [class, x1, y1, x2, y2]
                            x1 and x2 lie between 0 and width of the image,
                            y1 and y2 lie between 0 and height of the image.

            You need to do the following, 
            1. Extract the correct annotation using the idx provided.
            2. Read the image and convert it into a numpy array (wont be necessary
                with some libraries). The shape of the array would be (3, H, W).
            3. Scale the values in the array to be with [0, 1].
            4. Create a dictonary with both the image and annotations
            4. Perform the desired transformations.
            5. Return the transformed image and annotations as specified.
        '''

        image = Image.open(self.img_data[idx]["path"])
        for curr_transform in self.transforms:
            image = curr_transform(image)

        gt_bboxes = list()
        for box in self.img_data[idx]["bboxes"]:
            data_list = box["bbox"]
            data_list.insert(0, box["category"])
            gt_bboxes.append(data_list)

        image_array = np.array(image)
        image_array = image_array.transpose(2, 0, 1) # convert to (3, H, W) from (H, W, 3)
        image_array = np.array(image_array, dtype = np.float32)
        image_array /= 255.0 # scale between  to 1
        img_dict = {"image" : image_array, "gt_bboxes" : gt_bboxes}
        return img_dict