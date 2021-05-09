import rawpy
import matplotlib.image as pltimg
import os

img_paths = [
    # "../WeatherNet/dataset2/800/IMG_2581.CR2",
    # "../WeatherNet/dataset2/800/IMG_2584.CR2",
    "../WeatherNet/dataset3/IMG_2635.CR2",
    "../WeatherNet/dataset3/IMG_2639.CR2"
]

for img_path in img_paths:
    img_name = os.path.basename(img_path).split('.')[0]
    with rawpy.imread(img_path) as raw:
        image_raw = raw.postprocess()
    home_dir = os.path.expanduser("~")
    img_new_path = f"{home_dir}/Downloads/{img_name}.jpg"
    print(img_new_path, image_raw.shape)
    pltimg.imsave(img_new_path, image_raw)