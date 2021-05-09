import cv2
import os

img_paths = [
    "../models/images/IMG_2635.jpg",
    "../models/images/IMG_2639.jpg",
]


for img_path in img_paths:
    image = cv2.imread(img_path)
    image = image[957:2017, 1935:3372, :]
    home_dir = os.path.expanduser("~")
    img_name = os.path.basename(img_path)
    img_path_new = f"{home_dir}/Downloads/{img_name}"
    print(img_path_new)
    cv2.imwrite(img_path_new, image)