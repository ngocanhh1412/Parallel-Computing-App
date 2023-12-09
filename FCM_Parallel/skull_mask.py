import cv2
import imageio
import numpy as np
import scipy.ndimage as ndi
from sklearn.mixture import GaussianMixture

class SkullMask:
    """
    The SkullMask class is designed to make the mask for skull from an input image. 
    It utilizes the Gaussian Mixture Model (GMM) for segmentation, morphological operations 
    for mask refinement, and contour analysis to identify and remove the skull region.

    Methods:
    - __init__(self, file_path): Initializes the RemoveMostSkull object with the path to the image file.
    - canny_edge(self, image, low_threshold=0, high_threshold=255): Applies the Canny edge detection algorithm.
    - find_contours(self, image): Finds contours in the image and returns the area of the largest contour.
    - apply_gmm_segmentation(self, image, n_components=4): Applies GMM segmentation to the input image.
    - skull_strip(self): Removes the skull from the input image using GMM segmentation.

    Attributes:
    - image (numpy.ndarray): The input image.
    """

    def __init__(self, image):
        """
        Initializes the RemoveMostSkull object with the path to the image file.

        Parameters:
        - file_path (str): The path to the image file.
        """
        self.image = image

    def canny_edge(self, image, low_threshold=0, high_threshold=255):
        """
        Applies the Canny edge detection algorithm to the input image.

        Parameters:
        - image (numpy.ndarray): The input image.
        - low_threshold (int): The lower threshold for edge detection (default: 0).
        - high_threshold (int): The higher threshold for edge detection (default: 255).

        Returns:
        - edges (numpy.ndarray): The edges detected in the image.
        """
        image = np.uint8(image)
        edges = cv2.Canny(image, low_threshold, high_threshold)
        return edges

    def find_contours(self, image):
        """
        Finds contours in the input image and returns the area of the largest contour.

        Parameters:
        - image (numpy.ndarray): The input image.

        Returns:
        - area (float): The area of the largest contour in the image.
        """
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        edges = self.canny_edge(blurred)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        areas = [cv2.contourArea(contour) for contour in sorted_contours]
        return np.max(areas)

    def apply_gmm_segmentation(self, image, n_components=4):
        """
        Applies Gaussian Mixture Model (GMM) segmentation to the input image.

        Parameters:
        - image (numpy.ndarray): The input image.
        - n_components (int): Number of components in the GMM (default: 4).

        Returns:
        - tumor_mask (numpy.ndarray): The binary mask indicating the tumor region.
        """
        image_flat = image.flatten().reshape(-1, 1)

        gmm = GaussianMixture(n_components=n_components, random_state=42)
        gmm.fit(image_flat)
        means = gmm.means_

        tumor_component_index = np.argmax(means)
        tumor_mask = gmm.predict(image_flat) == tumor_component_index
        tumor_mask = tumor_mask.reshape(image.shape)

        return tumor_mask


    def skull_strip(self):
        """
        Removes the skull from the input image using Gaussian Mixture Model (GMM) segmentation.

        Returns:
        - skull (numpy.ndarray): Binary mask indicating the region of the skull.
        """
        self.image = self.image.astype(np.float32)

        # Apply GMM segmentation to create a mask with elements representing the tumor or skull
        mask = self.apply_gmm_segmentation(self.image)
        skull_mask = mask.copy()
        skull_mask = skull_mask.astype(np.float32)

        # Use morphological operations to refine the mask, then appling the refined mask to the original image
        kernel = np.ones((3, 3), dtype=np.float32)
        skull_mask = cv2.dilate(skull_mask, kernel, iterations=1)
        stripped_image = cv2.bitwise_and(self.image, skull_mask)

        labels, n_label = ndi.label(stripped_image)

        # Initialize an empty list to store the areas of each labeled component
        area_label = []
        for i in range(1, n_label):
            img_test = stripped_image.copy()
            mask_1 = labels == i
            mask_1 = mask_1.astype(np.float32)
            img_test = cv2.bitwise_and(img_test, mask_1)
            normalized_img = img_test / img_test.max()
            img_8bit = (normalized_img * 255).astype(np.uint8)
            area_label.append(self.find_contours(img_8bit))

        label_max_area = area_label.index(np.max(area_label)) + 1

        # Create a binary mask indicating the region of the skull based on the maximum area component
        skull = labels == label_max_area
        skull = skull.astype(np.float32)

        return skull

# import cv2
# import numpy as np
# import scipy.ndimage as ndi
# from sklearn.mixture import GaussianMixture

# class SkullMask:
#     def __init__(self, image):
#         self.image = image

#     def canny_edge(self, image, low_threshold=0, high_threshold=255):
#         image = np.uint8(image)
#         edges = cv2.Canny(image, low_threshold, high_threshold)
#         return edges

#     # def find_contours(self, image):
#     #     # Áp dụng GaussianBlur để giảm nhiễu và làm mờ ảnh
#     #     blurred = cv2.GaussianBlur(image, (5, 5), 0)

#     #     # Áp dụng ngưỡng để tạo ảnh nhị phân
#     #     edges = self.canny_edge(blurred)

#     #     # Tìm contour trong ảnh nhị phân
#     #     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     #     return cv2.contourArea(contours[0])

#     def find_contours(self, image):
#         # Áp dụng GaussianBlur để giảm nhiễu và làm mờ ảnh
#         blurred = cv2.GaussianBlur(image, (5, 5), 0)

#         # Áp dụng ngưỡng để tạo ảnh nhị phân
#         edges = self.canny_edge(blurred)

#         # Tìm contour trong ảnh nhị phân
#         contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#         sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

#         areas = [cv2.contourArea(contour) for contour in sorted_contours]
#         return np.max(areas)

#     def apply_gmm_segmentation(self, image, n_components=4):
#         image_flat = image.flatten().reshape(-1, 1)

#         gmm = GaussianMixture(n_components=n_components, random_state=42)
#         gmm.fit(image_flat)

#         means = gmm.means_

#         tumor_component_index = np.argmax(means)

#         tumor_mask = gmm.predict(image_flat) == tumor_component_index
#         tumor_mask = tumor_mask.reshape(image.shape)

#         return tumor_mask


#     def skull_strip(self):
#         '''
#         This function remove skull by using GMM to create mask that has elements same as tumor or skull
#         Then morpholorize mask labeling its elements, for each labels, using contour alg to find area, 
#         the largest area belongs to skull.
#         '''
#         mask = self.apply_gmm_segmentation(self.image)

#         skull_mask = mask.copy()
#         skull_mask = skull_mask.astype(np.float32)

#         kernel = np.ones((3,3), dtype=np.float32)
#         skull_mask = cv2.dilate(skull_mask, kernel, iterations=1)

#         stripped_image = cv2.bitwise_and(self.image, skull_mask)

#         labels, n_label = ndi.label(stripped_image)

#         area_label = []

#         for i in range(1, n_label):
#             img_test = stripped_image.copy()
#             mask_1 = labels == i
#             mask_1 = mask_1.astype(np.float32)

#             img_test = cv2.bitwise_and(img_test, mask_1)

#             # Chuẩn hóa giá trị của ảnh
#             normalized_img = img_test / img_test.max()
#             img_8bit = (normalized_img * 255).astype(np.uint8)

#             area_label.append(self.find_contours(img_8bit))
        
#         label_max_area = area_label.index(np.max(area_label)) + 1

#         skull = labels == label_max_area
#         skull = skull.astype(np.float32)
        
#         return skull