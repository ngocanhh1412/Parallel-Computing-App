import cv2
import numpy as np
import scipy.ndimage as ndi
from sklearn.mixture import GaussianMixture

class SkullMask:
    def __init__(self, image):
        self.image = image

    def canny_edge(self, image, low_threshold=0, high_threshold=255):
        image = np.uint8(image)
        edges = cv2.Canny(image, low_threshold, high_threshold)
        return edges

    # def find_contours(self, image):
    #     # Áp dụng GaussianBlur để giảm nhiễu và làm mờ ảnh
    #     blurred = cv2.GaussianBlur(image, (5, 5), 0)

    #     # Áp dụng ngưỡng để tạo ảnh nhị phân
    #     edges = self.canny_edge(blurred)

    #     # Tìm contour trong ảnh nhị phân
    #     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #     return cv2.contourArea(contours[0])

    def find_contours(self, image):
        # Áp dụng GaussianBlur để giảm nhiễu và làm mờ ảnh
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # Áp dụng ngưỡng để tạo ảnh nhị phân
        edges = self.canny_edge(blurred)

        # Tìm contour trong ảnh nhị phân
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        areas = [cv2.contourArea(contour) for contour in sorted_contours]
        return np.max(areas)

    def apply_gmm_segmentation(self, image, n_components=4):
        image_flat = image.flatten().reshape(-1, 1)

        gmm = GaussianMixture(n_components=n_components, random_state=42)
        gmm.fit(image_flat)

        means = gmm.means_

        tumor_component_index = np.argmax(means)

        tumor_mask = gmm.predict(image_flat) == tumor_component_index
        tumor_mask = tumor_mask.reshape(image.shape)

        return tumor_mask


    def skull_strip(self):
        '''
        This function remove skull by using GMM to create mask that has elements same as tumor or skull
        Then morpholorize mask labeling its elements, for each labels, using contour alg to find area, 
        the largest area belongs to skull.
        '''
        mask = self.apply_gmm_segmentation(self.image)

        skull_mask = mask.copy()
        skull_mask = skull_mask.astype(np.float32)

        kernel = np.ones((3,3), dtype=np.float32)
        skull_mask = cv2.dilate(skull_mask, kernel, iterations=1)

        stripped_image = cv2.bitwise_and(self.image, skull_mask)

        labels, n_label = ndi.label(stripped_image)

        area_label = []

        for i in range(1, n_label):
            img_test = stripped_image.copy()
            mask_1 = labels == i
            mask_1 = mask_1.astype(np.float32)

            img_test = cv2.bitwise_and(img_test, mask_1)

            # Chuẩn hóa giá trị của ảnh
            normalized_img = img_test / img_test.max()
            img_8bit = (normalized_img * 255).astype(np.uint8)

            area_label.append(self.find_contours(img_8bit))
        
        label_max_area = area_label.index(np.max(area_label)) + 1

        skull = labels == label_max_area
        skull = skull.astype(np.float32)
        
        return skull
