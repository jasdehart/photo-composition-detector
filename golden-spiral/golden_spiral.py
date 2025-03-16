from PIL import Image

import matplotlib.pyplot as plt
import numpy as np

from ultralytics import YOLO
import pandas as pd
import glob
import math



def compute_spiral(topleft, topright, bottomright, pic, resolution=1000):
    def find_slope_intercept(point1, point2):
        # Get the x and y values for each point
        x1, y1 = point1
        x2, y2 = point2
        
        # Calculate the slope of the line
        slope = (y2 - y1) / (x2 - x1)
        
        # Calculate the y-intercept of the line
        y_intercept = y1 - slope * x1
        
        return slope, y_intercept

    def find_intersection(line1, line2):
        # Unpack the slopes and y-intercepts of the lines
        m1, b1 = line1
        m2, b2 = line2
        
        # Solve for x using the equation m1 * x + b1 = m2 * x + b2
        x = (b2 - b1) / (m1 - m2)
        
        # Calculate the y value for the intersection point using either line equation
        y = m1 * x + b1
        
        return x, y

    line1 = find_slope_intercept(topleft, bottomright)
    line2 = find_slope_intercept((bottomright[0]/1.6,bottomright[1]), topright)

    x0,y0 = find_intersection(line1, line2)

    # Load image
    img = np.asarray(Image.open(pic))

    # Golden Ratio and Spiral Parameters
    phi = (1 + 5**0.5) / 2
    y0 = 1 / (2 + phi)
    x0 = (2 * phi + 1) * y0
    theta0 = np.arctan2(-y0, -x0)
    k = 2 * np.log(phi) / np.pi
    a = -x0 / (np.exp(k * theta0) * np.cos(theta0))

    # Define the spiral equation
    t = np.linspace(-20, theta0, 1000)
    def x(t): return x0 + a * np.exp(k * t) * np.cos(t)
    def y(t): return y0 + a * np.exp(k * t) * np.sin(t)

    # Image dimensions
    height, width = img.shape[:2]

    # Calculate max extents of the spiral (ignoring scaling for now)
    max_x = np.max(np.abs(x(t)))
    max_y = np.max(np.abs(y(t)))

    # Find scaling factors
    scale_x = width / max_x  # Scale the spiral to fit the width
    scale_y = height / max_y  # Scale the spiral to fit the height

    # Use the smaller scaling factor to avoid surpassing either dimension
    scale = min(scale_x, scale_y)

    # Apply the scaling to the spiral
    scaled_x = scale * (x(t) - x0)
    scaled_y = scale * (y(t) - y0)

    # Calculate dynamic offsets (relative to image dimensions)
    offset_x = width * 0.72 # Adjust this proportion to move the spiral horizontally
    offset_y = height * 0.3 # Adjust this proportion to move the spiral vertically

    # Shift the spiral to start at the dynamic offset
    scaled_x += offset_x
    scaled_y += offset_y

    return img, scaled_x, scaled_y



def closest_point_and_distance(point_list, box_coord_x, box_coord_y, box_width, box_length):
    
    center_x = (box_coord_x + box_width) / 2
    center_y = (box_coord_y + box_length) / 2 

    
    min_distance = math.inf
    closest_point= None


    for point in point_list:
        distance = math.sqrt((point[0]-center_x)**2 + (point[1]-center_y)**2)
        if distance < min_distance:
            min_distance = distance
            closest_point = point

    x = [center_x,closest_point[0]]
    y = [center_y, closest_point[1]]

    plt.plot(x,y, marker='v', color="yellow")
    plt.plot(center_x, center_y, marker='v', color="blue") 
    plt.text(x[-1],y[-1], f'{min_distance:.2f}')

    return closest_point[0], closest_point[1], center_x, center_y, min_distance


def draw_golden_spiral(img, point_list_x, point_list_y, line_width=3):
    # , conn_point_x, conn_point_y, line_color=(60, 90, 205), line_width=3):
    """
    Helper Function: Draws the lines on the img,

    Args:
        img: ImageObject
        img_path: STR save image to location specified
        start_point_x: INT x coordinate for starting point on line
        start_point_y: INT y coordinate for starting point on line
        end_point_x: INT x coordinate for end point on line
        end_point_y: INT y coordinate for end point on line

    Returns:
        start_point TUPLE, end_point TUPLE, edit_img ImageObject

    """

    img = np.asarray(Image.open(img))
    
    # Plotting the image and the spiral
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.plot(point_list_x, point_list_y, color='red', linewidth=line_width)

    plt.axis('off')
    plt.grid(False)





# model loader and data handler
model = YOLO("yolo11n.pt")

img_folder = '../images/'
files = []
for file in glob.glob(img_folder+"*.jpeg"):
    files.append(file)

import os

# Ensure the image folder exists
image_save_path = "./augmented_images/"
if not os.path.exists(image_save_path):
    os.makedirs(image_save_path)  # Create the folder if it doesn't exist


results = model.predict(source=files, save=False)

res_data = []
for res in results:
    img_path = res.path
    img_rename = img_path.split('/')[-1].split('.')[0]
    img_suffix= '-bounded.jpeg'
    img_save = image_save_path+img_rename+img_suffix
    img_height, img_width = res.orig_shape
    
    obdata = []
    for _, object in enumerate(res.boxes):
        print(object.xyxy)
        data = {'objectid': object.cls,
                'x': object.xyxy[0][0],
                'y': object.xyxy[0][1],
                'width':object.xyxy[0][2],
                'length':object.xyxy[0][3],
                'conf': object.conf}
        obdata.append(data)

    res.save(img_save)
    res_data.append([res.path, img_save, img_height, img_width, obdata])


img_data_df = pd.DataFrame(res_data, columns=['image', 'saved', 'height', 'width', 'object_data'])



### main.py
for m, img in img_data_df.iterrows():
        
    bounding_pic = f"{img['image']}"

    topleft = (0,0)
    topright = (0,img['height'])
    bottomright = (img['width'],0)

    img_np, point_list_x, point_list_y = compute_spiral(topleft, topright, bottomright, bounding_pic, resolution=10000)
    draw_golden_spiral(img['saved'], point_list_x, point_list_y)

    for i, item in enumerate (img['object_data']):
        connecting_x, connecting_y, box_center_x, box_center_y, dist = closest_point_and_distance(list(zip(point_list_x, point_list_y)), item['x'], item['y'], item['width'], item['length'])

    plt.savefig(f"{img['saved']}")
    plt.clf()