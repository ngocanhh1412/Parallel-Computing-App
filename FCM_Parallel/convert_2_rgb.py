from colorsys import hsv_to_rgb
import cv2
import numpy as np 
import matplotlib.pyplot as plt
class Convert2RGB:
    """
    Class for converting DICOM images to RGB format.

    This class provides methods to convert DICOM images to grayscale and then to RGB format.
    It also includes functions for handling intensity scaling and RGB color conversion.

    Methods:
    - convert2Gray(img): Converts a DICOM image to grayscale.
    - getRGB(val, minval, maxval): Converts a grayscale value to RGB color.
    - convert2Uint8(img, target_type_min, target_type_max, target_type): Scales image intensity to uint8 range.
    - convert2RGB(): Converts a DICOM image to RGB format.

    Args:
    - image (ndarray): Input DICOM image.

    Attributes:
    - image (ndarray): Input DICOM image.
    """

    def __init__(self, image):
        self.image = image 

    # convert from dcm to rgb
    def convert2Gray(self, img):
        """
        Converts a DICOM image to grayscale.
        Algorithm:
        1. Resize input image to 512x512 pixels.
        2. Normalize pixel values.
        3. Map intensity values to 256 grayscale bins.
        4. Create a 512x512 matrix (F) to store mapped values.
        5. Iterate through pixels, map intensity to bins, and store in F.
        6. Return F as grayscale image.
        """
        img = cv2.resize(img, (512, 512))

        A = np.zeros([512, 512])

        for i in range(512):
            for j in range(512):
                A[i][j] = img[i][j]

        amax = A.max()
        amin = A.min()
        A = A - amin

        ssize = amax - amin
        amax, amin = A.max(), A.min()

        bbin = ssize/255

        index = np.zeros([256])
        for i in range(256):
            index[i] = bbin*(i+1)

        F = np.zeros([512, 512])  # Chỉnh kích thước thành 512x512
        k = 0

        for i in range(512):  # Chỉnh kích thước thành 512
            for j in range(512):  # Chỉnh kích thước thành 512
                run = 1
                k = 0
                less = 0
                great = 0
                while(run == 1):
                    if(A[i][j] <= index[k]):
                        if(great == 1):
                            F[i][j] = k
                            run = 0
                            break

                        if(less == 1):
                            F[i][j] = k-1
                            run = 0
                            break

                        k = k+1
                        less = 1
                    else:
                        great = 1
                        k = k+1
                    if(k == 255):
                        F[i][j] = 255
                        break
        return F

    def getRGB(self, val, minval,  maxval):
        """
        Converts a grayscale value to RGB color.
        """
        h = (float(val-minval)/(maxval-minval)) * 255
        r, g, b = hsv_to_rgb(h/255, 1., 1.)
        return r, g, b

    def convert2Uint8(self, img, target_type_min, target_type_max, target_type):
        """
        Scales image intensity to uint8 range.
        """
        imin = img.min()
        imax = img.max()

        a = (target_type_max - target_type_min) / (imax - imin)
        b = target_type_max - a * imax
        new_img = (a * img + b).astype(target_type)
        return new_img

    def convert2RGB(self):
        """
        Converts a DICOM image to RGB format.
        """
        img_grey = self.convert2Gray(self.image)

        img_rgb = np.zeros(shape=(512,512,3), dtype=np.float64)
        img_rgb[:,:,0] = img_grey
        img_rgb[:,:,1] = img_grey
        img_rgb[:,:,2] = img_grey

        img = self.convert2Uint8(img_rgb, 0, 255, np.uint8)

        return img