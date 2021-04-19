#Imports
import numpy as np
import matplotlib.pyplot as plt
from my_package.model import ObjectDetectionModel
from my_package.data import Dataset
from my_package.analysis import plot_boxes
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage

def experiment(annotation_file, detector, transforms, outputs):
    '''
        Function to perform the desired experiments

        Arguments:
        annotation_file: Path to annotation file
        detector: The object detector
        transforms: List of transformation classes
        outputs: path of the output folder to store the images
    '''

    # Create the instance of the dataset.
    data_obj = Dataset(annotation_file)

    img_list = list()
    fig = plt.figure()
    titles = ["Original Image", "Horizontally Flipped Image", "Blurred Image", "2x Rescaled Image", "0.5x Rescaled Image", "90 Degree Right Rotated Image", "45 Degree Left Rotated Image"]

    # Iterate over all data items.
    for i, data in enumerate(data_obj):
        print("Plotting boundary boxes for image " + str(i))

        # Get the predictions from the detector.
        image_array = data["image"]
        pred_boxes, pred_class, pred_score = detector(image_array)
        predictions = {"pred_boxes" : pred_boxes, "pred_class" : pred_class, "pred_score" : pred_score}
        image_array *= 255.0
        image_array = np.array(image_array.transpose(1, 2, 0), dtype = np.uint8)

        # Draw the boxes on the image and save them.
        image = plot_boxes(image_array, predictions, outputs, str(i) + "_pred.jpg")
        if(i == 8):
            img_list.append(fig.add_subplot(2, 4, 1))
            img_list[-1].set_title(titles[0])  
            plt.imshow(image)
    print()

    # Do the required analysis experiments.
    print("Performing analysis task (a)") # this is already done in the upper loop
    for i, obj in enumerate(transforms):
        d_obj = Dataset(annotation_file, [obj])
        print("Performing analysis task (" + chr(98 + i) + ")")
        image_array = d_obj[8]["image"]
        pred_boxes, pred_class, pred_score = detector(image_array)
        predictions = {"pred_boxes" : pred_boxes, "pred_class" : pred_class, "pred_score" : pred_score}
        image_array *= 255.0
        image_array = np.array(image_array.transpose(1, 2, 0), dtype = np.uint8)
        image = plot_boxes(image_array, predictions, outputs, "8_" + chr(98 + i) + ".jpg")
        img_list.append(fig.add_subplot(2, 4, i + 2))
        img_list[-1].set_title(titles[i + 1])  
        plt.imshow(image)
    print()

    plt.show()


def main():
    detector = ObjectDetectionModel()
    experiment('./data/annotations.jsonl', detector, [FlipImage("horizontal"), BlurImage(3), RescaleImage(2.0), RescaleImage(0.5), RotateImage(270), RotateImage(45)], "./output_imgs") # Sample arguments to call experiment()


if __name__ == '__main__':
    main()