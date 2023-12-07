import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


class FCM():
    def __init__(self, image, image_bit, n_clusters, m, epsilon, max_iter):
        self.image = image
        self.image_bit = image_bit
        self.n_clusters = n_clusters
        self.m = m
        self.neighbour_effect = 3
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.kernel_size = 5

        self.shape = image.shape  # image shape
        # flatted image shape: (number of pixels,1)
        self.X = image.flatten().astype('float')
        self.numPixels = image.size
        self.U = np.zeros((self.numPixels, self.n_clusters))
        self.C = None

    def get_mean_image_in_window(self, image, kernel):
        '''Get image consisting of mean values ​​of neighboring pixels in a window '''    
        neighbor_sum = convolve2d(
            image, kernel, mode='same',
            boundary='fill', fillvalue=0)

        num_neighbor = convolve2d(
            np.ones(image.shape), kernel, mode='same',
            boundary='fill', fillvalue=0)

        return neighbor_sum / num_neighbor  
    def get_filtered_image(self):
        
         # Create padding image
        print("Getting filtered image..") 
        
        # mask to ignore the center pixel
        mask = np.ones((self.kernel_size,self.kernel_size))
        mask[int(self.kernel_size/2),int(self.kernel_size/2)]=0
        
        a = self.neighbour_effect # alpha
        mean_image = self.get_mean_image_in_window(self.image, mask)
        # median_image = ndimage.generic_filter(self.image, np.nanmean, footprint=mask, mode='constant', cval=np.NaN) # too slow
        filtered_image = (self.image+a*mean_image)/(1+a) # linearly-weighted sum image
        dtype = self.image.dtype
        self.filtered_image = filtered_image.reshape(self.shape).astype(dtype)
    
    def calculate_histogram(self):        
        hist_max_value = (1 << self.image_bit)
        hist = cv2.calcHist([self.filtered_image],[0],None,[hist_max_value],[0,hist_max_value])
        self.num_gray = len(hist)
        self.histogram = hist
    def initial_U(self):
        idx = np.arange(self.numPixels)
        
        for ii in range(self.n_clusters):
            idxii = idx % self.n_clusters == ii
            self.U[idxii, ii] = 1
        return self.U
    
    def update_U(self):
        '''Compute weights'''
        c_mesh, idx_mesh = np.meshgrid(self.C, self.X)
        power = 2./(self.m-1)
        p1 = abs(idx_mesh-c_mesh)**power
        p2 = np.sum((1./abs(idx_mesh-c_mesh))**power, axis=1)

        return 1./(p1*p2[:, None])
    
    def matrix_mul(a, b, c):

        for i in range(1):
            for j in range(len(c)):
                # Initialize the element in the result matrix to 0
                c[i][j] = 0
                for k in range(len(b)):
                    # Multiply corresponding elements and accumulate the result
                    c[i][j] += a[i][k] * b[k][j]


    def update_C(self):
        '''Compute centroid of clusters'''
        numerator = np.dot(self.X, self.U**self.m)
        # print("Shapes:", self.X, self.U**self.m)  # Add this line to check the shapes
        # U_m = self.U**self.m
        # numerator = np.zeros((1, self.U.shape[1]))
        
        # for j in range(self.U.shape[1]):
        #     for k in range(len(self.U)):
        #         numerator[0][j] += self.X[k] * U_m[k][j]

        
        denominator = np.sum(self.U**self.m, axis=0)
        return 1.*numerator/denominator

    def form_clusters(self):
        self.get_filtered_image() 
        self.calculate_histogram()
        '''Iterative training'''
        d = 100
        self.U = self.initial_U()
        if self.max_iter != -1:
            i = 0
            while True:
                self.C = self.update_C()
                old_u = np.copy(self.U)
                self.U = self.update_U()
                d = np.sum(abs(self.U - old_u))
                # print("Iteration %d : cost = %f" % (i, d))

                if d < self.epsilon or i > self.max_iter:
                    break
                i += 1
        else:
            i = 0
            while d > self.epsilon:
                self.C = self.update_C()
                old_u = np.copy(self.U)
                self.U = self.update_U()
                d = np.sum(abs(self.U - old_u))
                print("Iteration %d : cost = %f" % (i, d))

                if d < self.epsilon or i > self.max_iter:
                    break
                i += 1
        return self.segmentImage()

    def deFuzzify(self):
        # center = np.uint8(self.U)
        return np.argmax(self.U, axis=1)

    def segmentImage(self):
        '''Segment image based on max weights'''

        result = self.deFuzzify()
        self.result = result.reshape(self.shape).astype('int')
        
        return (self.U, self.C)