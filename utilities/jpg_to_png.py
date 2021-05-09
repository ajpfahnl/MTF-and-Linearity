import cv2
import os

# use the ImageMagick convert utility instead

rcdpath = "../models/RCDNet/RCDNet_code/for_spa/data/test/small/"

img_paths = [
    rcdpath + "norain/" + "1_cropped.jpg",
    rcdpath + "norain/" + "2_cropped.jpg",
    rcdpath + "rain/" + "1_cropped.jpg",
    rcdpath + "rain/" + "2_cropped.jpg",
]

for img_path in img_paths:
    image = cv2.imread(img_path)
    img_path = os.path.split(img_path)
    img_name = img_path[-1].split('.')[0]
    img_path_new = os.path.join(*img_path[:-1], img_name) + ".png"
    cv2.imwrite(img_path_new, image)