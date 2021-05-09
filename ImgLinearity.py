import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

class ImgLinearity():
    sRGB_R = np.array([115, 194, 98, 87, 133, 103,
                        214, 80, 193, 94, 157, 224, 
                        56, 70, 175, 231, 187, 8, 
                        243, 200, 160, 122, 85, 52])
    sRGB_G = np.array([82, 150, 122, 108, 128, 189,
                        126, 91, 90, 60, 188, 163, 
                        61, 148, 54, 199, 86, 133,
                        243, 200, 160, 122, 85, 52])
    sRGB_B = np.array([68, 130, 157, 67, 177, 170,
                        44, 166, 99, 108, 64, 46,
                        150, 73, 60, 31, 149, 161,
                        242, 200, 160, 121, 85, 52])

    def __init__(self, img_color, square_space = None, offset_x = None, offset_y = None):
        s = (img_color.shape[0], img_color.shape[1])
        img_R = np.zeros(s)
        img_G = np.zeros_like(img_R)
        img_B = np.zeros_like(img_R)
        img_R = img_color[:, :, 0]
        img_G = img_color[:, :, 1]
        img_B = img_color[:, :, 2]

        self.img_R = img_R
        self.img_G = img_G
        self.img_B = img_B

        square_space = int(s[1]//6)
        offset_y = square_space//2
        offset_x = square_space//2

        target_locs = np.zeros((4, 6, 2), dtype='int')
        for i in range(4):
            for j in range(6):
                target_locs[i, j, 1] = i*square_space + offset_x # x
                target_locs[i, j, 0] = j*square_space + offset_y # y 
        target_locs = target_locs.reshape((24, 2))

        self.target_locs = target_locs

    def extract_actual(self, box=None):
        target_locs = self.target_locs
        R_actual = np.zeros(24)
        G_actual = np.zeros(24)
        B_actual = np.zeros(24)

        if box == None:
            R_actual = self.img_R[target_locs[:, 1], target_locs[:, 0]]
            G_actual = self.img_G[target_locs[:, 1], target_locs[:, 0]]
            B_actual = self.img_B[target_locs[:, 1], target_locs[:, 0]]
        else:
            for n, (i, j) in enumerate(zip(target_locs[:, 1], target_locs[:, 0])):
                R_actual[n] = np.average(self.img_R[i:i+box, j:j+box])
                G_actual[n] = np.average(self.img_G[i:i+box, j:j+box])
                B_actual[n] = np.average(self.img_B[i:i+box, j:j+box])

        self.R_actual = R_actual
        self.G_actual = G_actual
        self.B_actual = B_actual

    def linregress(self, x, y):
        reg = LinearRegression().fit(x[:, np.newaxis], y)
        return reg.predict(x[:, np.newaxis])

    def plot(self):
        fig, axs = plt.subplots(1,3)
        axs[0].scatter(self.sRGB_R, self.R_actual, color='r')
        axs[0].plot(self.sRGB_R, self.linregress(self.sRGB_R, self.R_actual), color='k')
        axs[0].set_title("Red")

        axs[1].scatter(self.sRGB_G, self.G_actual, color='g')
        axs[1].plot(self.sRGB_G, self.linregress(self.sRGB_G, self.G_actual), color='k')
        axs[1].set_title("Green")

        axs[2].scatter(self.sRGB_B, self.B_actual, color='b')
        axs[2].plot(self.sRGB_B, self.linregress(self.sRGB_B, self.B_actual), color='k')
        axs[2].set_title("Blue")

        [ax.set_xlabel('Ideal sRGB') for ax in axs]
        [ax.set_ylabel('Measured Intensity') for ax in axs]

        fig.tight_layout()
        fig.set_figwidth(15)