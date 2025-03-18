import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import os


# helper modules
import argparse
import logging


def extract_features(image_path):
    '''
    Function to extract features from an image using the ORB detector.
    
    Args:
        image_path: str, path to the image file from which to extract features.
    
    Return:
        descriptors: numpy.ndarray, descriptors of keypoints detected in the image.
    '''
    logging.info(f'Extracting features for {image_path}')
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors
    keypoints, descriptors = orb.detectAndCompute(img, None)

    return descriptors


def compare_images(image1_path, image2_path):
    '''
    Function to compare two images and calculate their similarity based on keypoint descriptors.
    
    Args:
        image1_path: str, path to the first image.
        image2_path: str, path to the second image.
    
    Return:
        similarity_score: float, a score between 0 and 1 indicating the similarity of the two images.
    '''
    descriptors1 = extract_features(image1_path)
    descriptors2 = extract_features(image2_path)

    logging.info(f'Comparing {image1_path} vs {image2_path}')

    # Check if descriptors were detected
    if descriptors1 is None or descriptors2 is None:
        print("No descriptors found in one or both images.")
        return 0  # Return zero similarity if no descriptors

    # Use BFMatcher (Brute-Force Matcher) for feature comparison
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(descriptors1, descriptors2)

    # If no matches were found, return zero similarity
    if len(matches) == 0:
        print("No matches found between the two images.")
        return 0

    # Sort matches based on distance (lower distance = more similar)
    matches = sorted(matches, key=lambda x: x.distance)

    # Calculate the average distance of the top matches
    top_matches = matches[:min(10, len(matches))]  # Consider top 10 matches, or all if there are fewer than 10
    avg_distance = np.mean([match.distance for match in top_matches])

    # Normalize the average distance to a similarity score
    # We assume that the minimum possible distance is 0, and the maximum distance is a large value, say 100
    similarity_score = 1 - (avg_distance / 100)

    # Ensure the similarity score is between 0 and 1
    similarity_score = max(0, min(1, similarity_score))

    return similarity_score


def image_similarity_search(query_image_path, image_folder_path):
    '''
    Function to search for images in a folder that are most similar to a query image.
    
    Args:
        query_image_path: str, path to the query image.
        image_folder_path: str, path to the folder containing images to compare with.
    
    Return:
        similarity_scores: list of tuples, where each tuple contains the image path and its similarity score to the query image.
    '''
    logging.info(f'Starting image similarity search')
    # Ensure the image folder exists
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)  # Create the folder if it doesn't exist
    
    # List all images in the folder
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Store similarity scores for each image
    similarity_scores = []

    # Compare query image with all images in the folder
    for image_file in image_files:
        image_path = os.path.join(image_folder_path, image_file)
        similarity_score = compare_images(query_image_path, image_path)
        similarity_scores.append((image_path, similarity_score))

    # Sort images by similarity score in descending order
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    # Return the sorted images with scores
    return similarity_scores


def show_images_side_by_side(image1_path, image2_path, similarity_score):
    '''
    Function to display two images side by side with their similarity score.
    
    Args:
        image1_path: str, path to the first image.
        image2_path: str, path to the second image.
        similarity_score: float, the similarity score between the two images to be displayed.
    
    Return:
        nothing, only displays the images.
    '''
    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # Convert from BGR (OpenCV) to RGB (Matplotlib)
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # Create a figure and set up two subplots (side by side)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Show the first image
    axes[0].imshow(img1_rgb)
    axes[0].set_title("Image 1")
    axes[0].axis('off')  # Hide axes

    # Show the second image
    axes[1].imshow(img2_rgb)
    axes[1].set_title("Image 2")
    axes[1].axis('off')  # Hide axes

    # Display similarity score in the center of the figure
    fig.suptitle(f"Similarity Score: {similarity_score:.2f}", fontsize=16)

    # Show the plot
    plt.show()


def display_results(query_image_path, image_folder_path):
    '''
    Function to display the results of the image similarity search, showing the most similar images and their similarity scores.
    
    Args:
        query_image_path: str, path to the query image.
        image_folder_path: str, path to the folder containing images to compare with.
    
    Return:
        nothing, only prints the results and displays images.
    '''
    results = image_similarity_search(query_image_path, image_folder_path)

    print(f"Most similar images to {query_image_path}:\n")

    for result in results:
        image_file, score = result
        print(f"Image: {image_file}, Similarity Score: {score:.2f}")
        show_images_side_by_side(query_image_path, image_file, score)


if __name__=="__main__":

    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )


    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--query", help="image for similarity", type=str, required=True)
    parser.add_argument("-f","--folder", help="folder for image similarity", type=str, required=True)
    parser.add_argument("-m","--model", help="model option for running", type=str, choices=["yolo-small", "yolo-ultra", "yolov11"], default='yolo-small')


    logging.info('Setting up variables')

    args = parser.parse_args()
    query_image_path = args.query
    image_folder_path = args.folder  # Folder with images to search from
    display_results(query_image_path, image_folder_path)
