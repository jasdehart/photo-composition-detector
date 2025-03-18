Got it! Below is the README in proper Markdown format with headers, bullet points, and formatting:

```markdown
# Image Similarity Comparison

This script compares an image to a folder of images using feature matching and displays the most similar images side by side along with the calculated similarity score. It leverages OpenCV's ORB feature detector and Brute-Force Matcher to compute similarity based on keypoint descriptors.

## Requirements

Before running the script, make sure you have the following libraries installed:

- Python 3.x
- OpenCV for image processing
- Matplotlib for displaying images
- Numpy for handling arrays
- Pillow (PIL) for image handling
- Logging for generating logs
- Argparse for parsing command-line arguments
- OS for file path handling

You can install the required dependencies using pip:

```bash
pip install opencv-python matplotlib numpy Pillow
```

## How to Use

1. **Prepare your images:**
    - Ensure you have a query image and a folder containing images to compare against.
    - You should have the images in accessible paths, either in the same directory as the script or provide the relative/absolute path to them.

2. **Run the script:**
    - Run the script from the command line using the following format:

    ```bash
    python image_similarity.py --query <query_image_path> --folder <image_folder_path>
    ```

    Replace `<query_image_path>` with the path to the image you want to compare, and `<image_folder_path>` with the path to the folder containing images for comparison.

    Example:

    ```bash
    python image_similarity.py --query image1.jpg --folder images/
    ```

    This will:
    - Load the query image and all images in the specified folder.
    - Perform feature matching between the query image and each image in the folder to calculate a similarity score.
    - Display the most similar images side by side, along with their similarity scores.

## Code Explanation

1. **Image Loading:**
    - The images are loaded using OpenCV’s `cv2.imread()` function.
    - Images are then converted from BGR (OpenCV format) to RGB (Matplotlib format) for proper display.

2. **Feature Extraction:**
    - The script uses the **ORB** (Oriented FAST and Rotated BRIEF) feature detector to extract keypoints and descriptors from the images.
    - **ORB** is efficient and works well for keypoint-based matching.

3. **Feature Matching:**
    - A **Brute-Force Matcher** (`cv2.BFMatcher`) is used to compare the descriptors between the two images.
    - A similarity score is computed based on the average distance of the top matches. This is normalized to a value between 0 and 1, where a higher value indicates higher similarity.

4. **Displaying Results:**
    - Matplotlib is used to display the query image and the most similar images side by side.
    - A similarity score is shown at the top of the displayed images.

5. **Image Similarity Search:**
    - The script compares the query image with all the images in a specified folder.
    - It returns the images with the highest similarity scores in descending order.

## Example Output

When running the script, you will see the most similar images to the query image displayed side by side, with their similarity scores shown at the top.

```text
Most similar images to image1.jpg:

Image: images/image2.jpg, Similarity Score: 0.85
[Image1]            [Image2]
Similarity Score: 0.85

Image: images/image3.jpg, Similarity Score: 0.75
[Image1]            [Image3]
Similarity Score: 0.75
```

The displayed images will be shown in Matplotlib's window, and the similarity score will appear in the center of the plot.

## Notes

- The images should be of a compatible format (JPEG, PNG, etc.) and should be properly accessible (i.e., the file paths should be correct).
- The similarity score is a value between 0 and 1:
    - A score closer to 1 indicates that the images are highly similar.
    - A score closer to 0 indicates low similarity or no significant matching features.
- The script will display the top results based on similarity scores, showing both the images and their calculated similarity.
  
## Logging

- The script includes logging, which will provide detailed information on the processes, including:
    - Image feature extraction
    - Image comparison steps
    - Similarity score calculation
  
- The log output will be saved in the terminal/console based on the log level set in the script (`INFO` level by default).

## Example Run

```bash
python image_similarity.py --query query_image.jpg --folder images/
```

This will compare `query_image.jpg` with all images in the `images/` folder, outputting the similarity scores and displaying the most similar images.
