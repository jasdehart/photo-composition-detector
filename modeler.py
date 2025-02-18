# perform object detection
# main modules
from PIL import Image
import torch

# submodules
from transformers import (
    AutoImageProcessor,
    AutoModelForObjectDetection,
)

def loadModel():

    '''
    Function to load Model and Processor
    return: image_processor, model
    '''
    image_processor = AutoImageProcessor.from_pretrained("hustvl/yolos-tiny", use_fast=False)  # prepares images for the model
    model = AutoModelForObjectDetection.from_pretrained("hustvl/yolos-tiny") #  Initializing a model (with random weights) from the hustvl/yolos-tiny style configuration
    return image_processor, model

def encodeImage(image_processor, image):
    '''
    Function to process given image
    return: inputs -> YolosImageProcessor values
    '''
    inputs = image_processor(images=image, return_tensors="pt")
    return inputs


def runModel(model, inputs):
    '''
    Function to run model with given input
    return: outputs
    '''
    outputs = model(**inputs)
    return outputs


def predictClass(image, image_processor, outputs):
    '''
    Function to prediction images: score, labels, bounds
    Bouding box coordinates are in Pascal VOC format [xmin, ymin, xmax, ymax]
    return: results
    
    target_sizes -> original image size 
    results -> a list of dictionaries with scores, labels, and boxes
    '''
    
    target_sizes = torch.tensor([image.size[::-1]]) #gets the original size of the image
    results = image_processor.post_process_object_detection(
        outputs, threshold=0.9, target_sizes=target_sizes
    )[0] # [0] accesses the list that is returned, we only get dictionary

    # pdb.set_trace()
    return results

