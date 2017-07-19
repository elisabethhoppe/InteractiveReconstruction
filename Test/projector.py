
from __future__ import division
from __future__ import print_function
from PIL import Image
from numpy import ones,vstack
from numpy.linalg import lstsq
from scipy.interpolate import RectBivariateSpline
from scipy import interpolate
import math
import matplotlib.pylab as plt
import numpy as np


def interpolation_Image(arr):
    x = np.arange(arr.shape[0])
    y = np.arange(arr.shape[1])
    z = arr
    img_interp_spline = RectBivariateSpline(x=x, y=y, z=arr, bbox=[None, None, None, None], kx=3, ky=3, s=0)
    return img_interp_spline


def radonRayDrivenApproach( arr,dSI, dDI, val, detectorSize, detectorSpacing, numProj):

        #Defining the fanogram image
        fanogram = Image.new('RGB', (377, 377), "black")  # create a new black image
        pixels = fanogram.load()

        detectorSizeIndex = (detectorSize / detectorSpacing)
        gammaM = math.atan((detectorSize / 2.0 - 0.5) / dSI)
        angRange = val + 2 * gammaM
        angStepSize = angRange / numProj
        samplingRate = 3.0
        maxbetaindex = angRange / angStepSize
        #print(maxbetaindex)

        #iterate over the rotation angle
        for i in np.arange(0, 10):
            #print(val)
            beta = val * i
            print(beta)
            cosBeta = math.cos(beta)
            sinBeta = math.sin(beta)

            #Compute source and detector points
            source_x = dSI * (cosBeta)
            source_y = dSI * sinBeta
            PP_Point_x = -detectorSize / 2 * sinBeta
            PP_Point_y = detectorSize / 2 * (cosBeta)
            PP = (PP_Point_x, PP_Point_y)
            source = (source_x, source_y)

            #Unit vector along the detector
            PP_vector = np.array(PP)
            PP_vector = np.multiply((-1),PP_vector)
            dirDetector = (PP_vector) / np.linalg.norm(PP_vector)


            #iterate over detector elements
            for t in range(0, int(detectorSizeIndex)):
                #calculate detector bin positions
                stepsDirection = 0.5 * detectorSpacing + t * detectorSpacing
                P = np.array(PP) + (dirDetector * stepsDirection)

                #Straight line equation between souce and the detector bin
                points = (source, P)
                distance = math.hypot(PP_Point_x - source_x, PP_Point_y - source_y)
                #        print("distance  " , distance)
                x_coords, y_coords = zip(*points)
                A = vstack([x_coords, ones(len(x_coords))]).T
                m, c = lstsq(A, y_coords)[0]
                straightline = "{m}x + {c}".format(m=m, c=c)

                #Normalised increment step
                increment = 1.0 / distance * samplingRate
                sum = 0.0

                #integral along the line
                for Linet in np.arange(0.0, distance * samplingRate):
                    current = np.array(source) + increment * Linet
                    #           print("current    ", current)
                    phantomWidth = 377
                    phantomHeight = 377
                    if ((phantomWidth) <= ((current.item(0)) + 1)) or ((phantomHeight) <= ((current.item(1)) + 1)) \
                            or ((current.item(0)) < 0) or ((current.item(1)) < 0):
                        continue
                    print("test    "  , current.item(0))
                    print("test2      " ,current.item(1))
                    print("test3      ", arr)
                    #fan_img = img_interp_spline(current.item(0), current.item(1))
                    #sum += np.interp( arr, current.item(0),current.item(1))
                #sum /= samplingRate
                #print("sum    ", sum)
                #pixels = (i, t, sum)
        #return fanogram


def plot_interp(image, img_):
    fig, axes = plt.subplots(1, 3)
    for ax, (im, text) in zip(axes, ((image, 'original'), (img_, 'interpolated'))):
        ax.imshow(im, cmap='gray')
        ax.title.set_text(text)
        ax.axis('off')

    plt.tight_layout(pad=0)
    plt.show()

'''
def radonRayDrivenApproach(img_interp_spline):
    for i in np.arange(0, 100):
        for j in np.arange(0, 100):
            img_ = img_interp_spline(i+0.5, j+0.5)
            print(img_)
            return img_
'''
        