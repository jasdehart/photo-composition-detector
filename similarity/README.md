# Image Similarity Comparison
This script compares two images using feature matching and displays them side by side along with the calculated similarity score.

## Requirements
Before running the script, make sure you have the following libraries installed:
*Python 3.x*
*OpenCV* for image processing
*Matplotlib* for displaying images
You can install these dependencies using pip:
```pip install opencv-python matplotlib```

## How to Use
Prepare your images:
Ensure you have two images to compare. Place the images in the same directory as the script or provide the relative/absolute path to the images.
For example, image1.jpg and image2.jpg.
Run the script from the command line with the following format:
```python image_similarity.py <image1_path> <image2_path>```

### Example:
```python image_similarity.py image1.jpg image2.jpg```

This will:
Load the two images specified in the command line.
Perform feature matching between the two images to calculate a similarity score.
Display the two images side by side with the similarity score at the top.

## Code Explanation
### Image Loading:
The images are loaded using OpenCV’s cv2.imread() function.
They are then converted from BGR (OpenCV format) to RGB (Matplotlib format).
### Feature Matching:
The images are compared using the ORB feature detector and descriptor.
A Brute-Force Matcher is used to compare the features between the two images.
A similarity score is calculated based on the average distance of the top matches.
### Displaying Images:
Matplotlib is used to display both images side by side, along with the calculated similarity score shown at the top.
#### Example Output
When running the script, you will see two images side by side with a similarity score displayed at the top:
-------------------------------------------
|         Image 1        |       Image 2        |
|    [Image here]        |   [Image here]        |
-------------------------------------------
    Similarity Score: 0.85
### Notes
The images should be of a compatible format (JPEG, PNG, etc.) and should be properly accessible.
The similarity score is between 0 and 1. A score closer to 1 indicates that the images are highly similar.
