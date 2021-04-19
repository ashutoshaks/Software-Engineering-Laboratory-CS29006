#Imports
import os
from PIL import Image, ImageDraw, ImageFont

def plot_boxes(image_array, predictions, outputs, filename): # Write the required arguments

    # The function should plot the predicted boxes on the images and save them.
    # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
    
    image = Image.fromarray(image_array)
    num_boxes = min(len(predictions["pred_boxes"]), 5)
    font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 20)
    for i in range(num_boxes):
        box = predictions["pred_boxes"][i]
        label = predictions["pred_class"][i]
        draw = ImageDraw.Draw(image)   
        draw.rectangle(box, outline = "black")
        draw.text((box[0][0], box[0][1] - 20), label, fill = "black", font = font, stroke_width = 1)
    image.save(os.path.join(outputs, filename))
    return image