## For Image Helpers and Handlers --- rot.py (main)
from PIL import ImageDraw
import math


### calculate points and lines for rot grid

def draw_line(img, start_point_x, start_point_y, end_point_x, end_point_y, line_color = (255, 0, 0), line_width = 3):
    """
    Helper Function: Draws the lines on the img,

    Args:
        img: ImageObject
        start_point_x: INT x coordinate for starting point on line
        start_point_y: INT y coordinate for starting point on line
        end_point_x: INT x coordinate for end point on line
        end_point_y: INT y coordinate for end point on line

    Returns:
        start_point TUPLE, end_point TUPLE, edit_img ImageObject
    """
    edit_img = ImageDraw.Draw(img)

    start_point = (start_point_x, start_point_y)
    end_point = (end_point_x, end_point_y)
    edit_img.line([start_point, end_point], fill=line_color, width=line_width)

    return start_point, end_point



def points_on_line(p1, p2):
    """
    Helper Function: Calculates evenly spaced points on the line defined by p1 and p2.

    Args:
        p1: Tuple (x, y) representing the first point.
        p2: Tuple (x, y) representing the second point.

    Returns:
        A list of tuples, each representing a point (x, y) on the line.
    """
    x1, y1 = p1
    x2, y2 = p2

    n = math.floor(math.dist(p1, p2))

    points = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0.5  # Avoid division by zero
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        points.append((x, y))
    return points


def vertical_line(width, side, grid=3):
    """
    Helper Function: Calculates the vertical line points.

    Args:
        width: INT of entire image
        grid: INT number of quadrants in thirds (3**1, 3**2, etc)
        side: STR indicates which side to split into thirds

    Returns:
        start_point_x INT, start_point_y INT, end_point_x INT, end_point_y INT
    """
    thirds = width// grid # divide the image into thirds

    match side: 
        case 'left':
            start_point_x = thirds # find starting point across width
            start_point_y = 0 # begin at starting point

            end_point_x = thirds # find end point across width
            end_point_y = width # end at bottom of image
        
        case 'right':
            start_point_x = width-thirds # find starting point across width
            start_point_y = 0 # begin at starting point

            end_point_x = width-thirds # find end point across width
            end_point_y = width # end at bottom of image

    return start_point_x, start_point_y, end_point_x, end_point_y

def horizontal_line(height, width, side, grid=3):
    """
    Helper Function: Calculates the horizontal line points.

    Args:
        height: INT of entire image
        width: INT of entire image
        grid: INT number of quadrants in thirds (3**1, 3**2, etc)
        side: STR indicates which side to split into thirds

    Returns:
        start_point_x INT, start_point_y INT, end_point_x INT, end_point_y INT
    """
    thirds = height// grid # divide the image into thirds

    match side: 
        case 'top':
            start_point_x = 0 # find starting point across width
            start_point_y = thirds # begin at starting point

            end_point_x = width # find end point across width
            end_point_y = thirds # end at bottom of image
        
        case 'bottom':
            start_point_x = 0 # find starting point across width
            start_point_y = height-thirds # begin at starting point

            end_point_x = width # find end point across width
            end_point_y = height-thirds # end at bottom of image

    return start_point_x, start_point_y, end_point_x, end_point_y


### compute object label

def computeItem(model, results):
    '''
    Function to map the model's output (dictionary) to the labels and bounding boxes.
    
    Args:
        model: Obj Detect Model
        results: DICT of model output
    
    Return:
        nothing, only print
    '''
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        print(
            f"Detected {model.config.id2label[label.item()]} with confidence "
            f"{round(score.item(), 3)} at location {box}"
        )

### calculate objects and distances for lines

def boundedImage(image, model, results):
    '''
    Function to draw image with bounding box

    Args:
        image: ImageObject
        model: ObjDetector
        results: ObjDetector prediction

    Return:
        width: INT bounding box width
        height: INT bounding box height
        coords: TUPLE of box coordinates
    '''
    width = image.width # get image width
    height = image.height # get image height

    for _, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        id2label = model.config.id2label[label.item()] # get labels for the preds

        box = [round(i, 2) for i in box.tolist()] # get bounding box coordinates
        x, y, w, h = tuple(box) # split bounding box coordinates
        # class_idx = label.item() # get class label

        if max(box) > 1.0:

            # Coordinates are un-normalized, no need to re-scale them
            x1, y1 = int(x), int(y)
            x2, y2 = int(x + w), int(y + h)

        else:

            # Coordinates are normalized, re-scale them
            x1 = int(x * width)
            y1 = int(y * height)
            x2 = int((x + w) * width)
            y2 = int((y + h) * height)
    
        # pdb.set_trace()
        draw = ImageDraw.Draw(image) # annotate existing image
        draw.rectangle((x1, y1, x2, y2), outline="yellow", width=2) # bounding box retangle
        draw.text(xy=((x2-x1)/2, (y2-y1)/2), text=id2label, fill="white") # add classification
    
    image.save("dog-bounds.jpg") # save bounded image
    return width, height, (x1,y1,x2,y2)


def closest_point_and_distance(box_coords, point_list):

    '''
    Function to find the closest point on lines to box center

    Args:
        box_coords: TUPLE bounding box coordinates
        point_list: LIST of points on the thirds line

    Return:
        closest_point: TUPLE of closest point
        center: TUPLE of box center
        min_distance: FLOAT of distance from points
    '''

    center_x = (box_coords[2]+box_coords[0])/2 
    center_y = (box_coords[3]+ box_coords[1])/2 

    min_distance = math.inf # arbitrary distance to be replace by minimums
    closest_point, numberp = None, None
    
    for p, point in enumerate(point_list):
        distance = math.sqrt(
        (point[0] - center_x) ** 2 + (point[1] - center_y) ** 2
        )
    
    if distance < min_distance:
        min_distance = distance
        closest_point = point
        numberp = p
   
    return closest_point, (center_x,center_y), min_distance
