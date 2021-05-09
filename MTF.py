import numpy as np
import scipy
from scipy import signal
from scipy.signal import argrelextrema
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt


class MTF():
    def __init__(self, img, center_offset = [0, 0], r_factor=1, raw=False, img_crop_params = None, rs=0):
        rs_orig = np.array([30, 40, 50, 60, 75, 100, 125, 150, 175, 200, 225, 250])

        if rs == 1:
            rs_orig = np.array([40, 50, 60, 75, 100, 125, 150, 175, 200, 225])
        
        center = [center_offset[0] + img.shape[0]//2, center_offset[1] + img.shape[1]//2]
        if raw:
            center[0] += 10
            center[1] += 10
        
        self.center = center
        if img_crop_params is not None:
            x_nw, y_nw, w, h = img_crop_params
            self.img = img[x_nw:x_nw+h, y_nw:y_nw+w]
        else:
            self.img = img

        self.rs = np.array(rs_orig*r_factor, dtype="int")

        self.ppm = img.shape[1]/190
        self.cpq = 36

        self.freqs = []
        self.freqs_orig = []
        for i in range(len(self.rs)):
            self.freqs.append(self.cpq*2 / (self.rs[i]/self.ppm * np.pi/4))
            self.freqs_orig.append(self.cpq*2 / (2 * np.pi * self.rs[i]))

        # self.Vw_loc = (img.shape[0]// (12/10), img.shape[1]//12.1)
        # self.Vb_loc = (img.shape[0]// (12/11), img.shape[1]//12.1)
        self.Vb = np.min(self.img)
        self.Vw = np.max(self.img)
    
    def find_arcs(self):
        img = self.img; rs = self.rs; center = self.center

        arcxs = []
        arcys = []
        arcvals = []
        for r in rs:
            arcval = []
            arcx = []
            arcy = []
            for i in range(-r, r+1):
                x = center[1] + i
                y = center[0] + int(np.sqrt(r**2 - i**2))
                arcx.append(x)
                arcy.append(y)
                arcval.append(img[y,x])
            arcxs.append(arcx)
            arcys.append(arcy)
            arcvals.append(arcval)
        self.arcvals, self.arcxs, self.arcys = arcvals, arcxs, arcys
        return arcvals, arcxs, arcys

    def display_arcs(self):
        img = self.img; center = self.center; arcvals = self.arcvals; arcxs = self.arcxs; arcys = self.arcys

        plt.gray()
        plt.imshow(img)
        plt.scatter([center[1]], [center[0]], marker='+')
        for i in range(len(arcxs)):
            plt.plot(arcxs[i], arcys[i])
        print(img.shape)

        # plt.scatter([self.Vw_loc[1]], [self.Vw_loc[0]])
        # plt.scatter([self.Vb_loc[1]], [self.Vb_loc[0]])

        print(f"{self.ppm} pixels per millimeter")
        print(f"{self.cpq} cycles per quadrant")
    
    def mtf_old(self, wave, Vb, Vw):
        Vmin = int(np.min(wave))
        Vmax = int(np.max(wave))
        C0 = (Vw - Vb)/(Vw + Vb)
        Cf = (Vmax - Vmin) / (Vmax + Vmin)
        return Cf/C0

    def mtf(self, wave, freq, filt=True, trim=10):
        # https://fakahil.github.io/solo/how-to-use-the-siemens-star-calibration-target-to-obtain-the-mtf-of-an-optical-system/index.html

        I = np.array(wave)

        if filt == False:
            yhat = I
        elif freq<0.45:
            yhat = savgol_filter(I, 11, 2)
        else:
            yhat = savgol_filter(I, 15, 2)
        
        if trim != 0:
            yhat = yhat[trim:-trim]

        maximums = scipy.signal.argrelextrema(yhat, np.greater,order=2)
        minimums = scipy.signal.argrelextrema(yhat, np.less,order=2)

        if len(maximums[0]) == 0:
            maximums = (np.array([np.argmax(yhat)]), )
        if len(minimums[0]) == 0:
            minimums = (np.array([np.argmin(yhat)]), )

        m = (yhat[maximums].mean() - yhat[minimums].mean())/(yhat[maximums].mean() + yhat[minimums].mean())
        return m

        

    def arcvals_to_mtfs_old(self):
        arcvals = self.arcvals
        
        Vb = self.Vb
        Vw = self.Vw
        Vb = min([int(min(arc)) for arc in arcvals])
        Vw = max([int(max(arc)) for arc in arcvals])
        mtfs = []
        for i in range(len(arcvals)):
            mtfs.append(self.mtf_old(arcvals[i], Vb, Vw))
        return mtfs

    def arcvals_to_mtfs(self, filt=True, trim=10):
        arcvals = self.arcvals
        
        # Vb = self.Vb
        # Vw = self.Vw
        # Vb = min([int(min(arc)) for arc in arcvals])
        # Vw = max([int(max(arc)) for arc in arcvals])
        mtfs = []
        for i in range(len(arcvals)):
            mtfs.append(self.mtf(arcvals[i], self.freqs_orig[i], filt, trim))
        mtfs = np.array(mtfs)
        
        Vb = np.min(mtfs)
        Vw = np.max(mtfs)

        C0 = (Vw - Vb)/(Vw + Vb)
        print(C0)
        mtfs = mtfs / C0
        self.mtfs = mtfs
        return mtfs