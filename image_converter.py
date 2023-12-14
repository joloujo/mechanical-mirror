from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import cv2 as cv
import warnings

warnings.filterwarnings('ignore') # Ignore warnings

class imageConverter():
    def __init__(self, width: int, height: int):
        """
        Initializes the image converter

        Args:
            width (int): The width of the mechanical mirror
            height (int): The height of the mechanical mirror
        """

        self.WIDTH = width
        self.HEIGHT = height
    
    def crop_to_aspect_ratio(self, image: np.ndarray):
        """
        Crops an image to the aspect ratio of the mechanical mirror

        Args:
            image (np.ndarray): The image to crop
        """

        # Get the dimensions of the original image
        current_height, current_width, _ = image.shape

        # Calculate the aspect ratio of the original image
        aspect_ratio = current_width / current_height

        # Define the target aspect ratio (20x15)
        target_aspect_ratio = self.WIDTH / self.HEIGHT

        # Calculate the new width and height for cropping
        if aspect_ratio > target_aspect_ratio:
            new_width = int(current_height * target_aspect_ratio)
            new_height = current_height
        else:
            new_width = current_width
            new_height = int(current_width / target_aspect_ratio)

        # Calculate the starting point for the crop
        start_x = (current_width - new_width) // 2
        start_y = (current_height - new_height) // 2

        # Crop the image
        cropped_image = image[start_y:start_y + new_height, start_x:start_x + new_width]

        return cropped_image

    def convert(self, background, picture):
        """
        Take two images and find which pixels on the mechanical mirror should be flipped

        Args:
            background (MatLike): The background image
            picture (MatLike): The image with the subject in it

        Returns:
            np.ndarray: A 2D array of booleans indicating which pixels should be on
        """

        # Convert BGR to HSV
        hsv1 = cv.cvtColor(background, cv.COLOR_BGR2HSV)
        hsv2 = cv.cvtColor(picture, cv.COLOR_BGR2HSV)

        # Extract the hue channel
        hue1 = hsv1[:, :, 2]
        hue2 = hsv2[:, :, 2]

        #find difference
        hue_difference = cv.absdiff(hue1, hue2)

        #find difference in total in normal format
        difference = cv.absdiff(picture, background)
        difference_gray = cv.cvtColor(difference, 7)


        #combine diff
        combined_image_diff = cv.absdiff(hue_difference, difference_gray)*2 + hue_difference/2 + difference_gray/2

        #Prep image to resize
        image_to_resize = Image.fromarray(combined_image_diff.astype('uint8'))

        #downsample image
        downsampled_image = image_to_resize.resize((self.WIDTH, self.HEIGHT))
        downsampled_image_array = np.asarray(downsampled_image)



        #Kmeans clustering separation
        flatten_array = downsampled_image_array.reshape(-1, 1)


        # Specify the number of clusters
        n_clusters = 3

        # Initialize the K-Means model
        kmeans = KMeans(n_clusters=n_clusters)

        # Fit the model to the data
        kmeans.fit(flatten_array)

        # Get the cluster assignments for each data point
        cluster_assignments = kmeans.labels_

        #reshape back into original shape
        final_image = cluster_assignments.reshape(self.HEIGHT, self.WIDTH)
        final_image = final_image[:, ::-1]

        #mask = np.logical_or(final_image == 1, final_image == 2)
        mask = final_image != final_image[1,1]

        inverted_mask = final_image == final_image[1,1]

        final_image[mask] = 1
        final_image[inverted_mask] = 0

        return final_image
