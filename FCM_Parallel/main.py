import imutils
from imutils import perspective
import cv2
import numpy as np
import matplotlib.pyplot as plt
from FCM import FCM
import imageio
from skull_mask import SkullMask
from convert_2_rgb import Convert2RGB
# import skfuzzy as fuzz

import os
from dotenv import load_dotenv
load_dotenv()
PATH2 = os.getenv("OUTPUT_PATH2")

def blur_image(img):
    # Áp dụng lọc trung bình
    kernel = np.ones((5,5),np.float32)/25
    blur = cv2.filter2D(img,-1,kernel)
    return blur

def tumor_part(c):
    area = cv2.contourArea(c)
    hull = cv2.convexHull(c)
    hull_area = cv2.contourArea(hull)
    if hull_area != 0:
        solidity = float(area)/hull_area
    else:
        solidity = 0

    if solidity > 0.5 and area > 500:
        return True
    else:
        return False
def threshold(img,b):
    # Phân ngưỡng
    ret,thresh = cv2.threshold(img,b,255,cv2.THRESH_BINARY)
    return thresh
def RGB(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
def contours(img,org,b):
    # img = RGB(img)
    img2 = threshold(img,b)
    # plt.imshow(img2)
    cnts = cv2.findContours(img2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    img2 = RGB(img2)
    org = RGB(org)
    for (_,c) in enumerate(cnts):
        if tumor_part(c):
            cv2.drawContours(org, [c], -1, (1,255,11), 2)
            cv2.drawContours(img2, [c], -1, (1,255,11), 2)

    return (org, img2)
def show_images(gray, blur, seg, cont_org, cont_mask):
    blur = cv2.resize(blur, (256, 256))
    seg  = cv2.resize(seg, (256, 256))
    cont_org = cv2.resize(cont_org, (256, 256))
    cont_mask = cv2.resize(cont_mask, (256, 256))
    seg_gray = cv2.cvtColor(seg, cv2.COLOR_BGR2GRAY)
    
    res1 =  np.hstack((blur,seg_gray))
    res2 =  np.hstack((cont_org,cont_mask))

    output_img_path = os.path.join(PATH2, "output_2.png")
    new_file_path = f"{output_img_path}"
    cv2.imwrite(new_file_path, res2)
def fcm(img, option):
    Z = img.reshape((-1, 1))
    Z = np.float32(Z)
    fuzz = FCM(image = Z, image_bit = 8, n_clusters = 8, m = 2, epsilon = 0.01, max_iter = 100, option= option)
    u, cntr = fuzz.form_clusters()
    #Nếu để code thư viện np.dot thì bỏ reshape này
    if(option != 1):
        cntr = cntr.reshape((8,1))
    print(f'{u.shape}, {cntr.shape}')

    labels = np.argmax(u, axis=1)
    center = np.uint8(cntr)
    res = center[labels]
    res2 = res.reshape(img.shape)
    return res2
def process(img3, b, option):
    gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    blur = blur_image(gray)
    seg = fcm(blur, option)
    plt.imshow(seg)
    cont_org, cont_mask = contours(seg, gray, b)
    # Convert 'result' to RGB for display
    seg = RGB(seg)

    gray = RGB(gray)
    show_images(gray, blur, seg, cont_org, cont_mask)

def main(path, option):
    gray = imageio.v2.imread(rf".\img\{path}")
    sk_mask = SkullMask(gray)
    output = sk_mask.skull_strip()

    a = np.where(output == 1)
    x, y = a[0], a[1]

    for (i, j) in zip(x, y):
        gray[i][j] = 0

    cv_2_rgb = Convert2RGB(gray)
    gray = cv_2_rgb.convert2RGB()

    process(img3=gray, b=130, option=option)

    output_img_path = os.path.join(PATH2, "output_2.png")
    new_file_path = f"{output_img_path}"
    return (new_file_path)
    
# if __name__ == '__main__':
#     path = "1-127.dcm"
#     main(path, option=1)