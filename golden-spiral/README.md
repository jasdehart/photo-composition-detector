# Golden Spiral Object Detection

## Overview
This project utilizes a YOLO (You Only Look Once) object detection model to detect objects in images and analyze their alignment with the golden spiral. The golden spiral is computed dynamically and overlaid on detected objects to visualize alignment.

## What is the Golden Spiral?
The golden spiral is a logarithmic spiral that grows outward by a factor of the golden ratio (approximately 1.618) for every quarter turn it makes. It is derived from the Fibonacci sequence and is commonly found in nature, art, and design. 

### Influence on Photo Composition
The golden spiral is often used in photography and visual arts to create a natural and aesthetically pleasing composition. It guides the viewer’s eye along a curved path, drawing attention to key elements within an image. Placing the focal point at or near the center of the spiral can create a sense of balance and harmony while also leading the viewer’s gaze through the scene organically.

## Features
- Uses [YOLO](https://github.com/ultralytics/ultralytics) for object detection.
- Computes and overlays a golden spiral on images.
- Finds the closest detected object to the spiral.
- Saves augmented images with the overlaid spiral and nearest object connections.

## Installation

### Prerequisites
Ensure you have Python installed and the required libraries:
```sh
pip install ultralytics pillow numpy matplotlib pandas glob2
```

### Using pyenv
You can use a pyenv as mentioned in the main repo. Details below:
```sh
pyenv install 3.11
pyenv virtualenv 3.11 composer
pyenv activate composer
pip install -r requirements.txt
```

## Usage

### 1. Place Images
Put the images you want to analyze in the `images/` folder.

### 2. Run the Script
```sh
python3 golden_spiral.py 
```

### 3. Output
- The processed images with the golden spiral and object connections are saved in the `augmented_images/` directory.

## Code Structure
- `compute_spiral()`: Computes the golden spiral overlay based on image dimensions.
- `closest_point_and_distance()`: Determines the closest object to the golden spiral.
- `draw_golden_spiral()`: Plots the golden spiral on the image.
- `golden_spiral.py`: Loads images, detects objects, and overlays the golden spiral.

## Example Output
After running the script, the processed images will have a golden spiral overlay and highlighted nearest objects.

![Example Output](golden-spiral/augmented_images/dog1-bounded.jpeg)


## Acknowledgments
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for object detection.
- Matplotlib and PIL for image processing.

