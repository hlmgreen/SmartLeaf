__author__ = 'markgreenwood'
import Image
from scipy import ndimage
#import matplotlib.pyplot as pyp
import scipy.stats
from scipy import misc
from scipy.ndimage import interpolation as inter
import numpy as np
import os
import shutil
import csv
import warnings

warnings.filterwarnings("ignore")
DataDict = {}


def setup_analysis():
    """Sets files up for analysis"""
    if os.path.exists('%s/Results' % file_path):
        shutil.rmtree('%s/Results' % file_path)  # removes preexisting results to prevent conflicts

    os.makedirs('%s/Results' % file_path)  # creates folder for results


def monochrome(picture, red, green, blue):
    """Converts green pixels to white and everything else to black"""
    black = (0, 0, 0)
    white = (255, 255, 255)
    xsize, ysize = picture.size
    temp = picture.load()

    for x in range(xsize):
        for y in range(ysize):
            r, g, b = temp[x, y]
            if r <= red and g >= green and b <= blue:
                temp[x, y] = white
            else:
                temp[x, y] = black


def average_images(j):
    """Opens, thresholds and then averages the 6 image copies at each time-point"""
    for i in range(1, img_nmb):
        im1 = Image.open('%s/Plate%s-%s-c0.png' % (file_path, j, i))
        monochrome(im1, 160, 150, 100)
        file1 = np.array(im1)

        im2 = Image.open('%s/Plate%s-%s-c1.png' % (file_path, j, i))
        monochrome(im2, 160, 150, 100)
        file2 = np.array(im2)

        im3 = Image.open('%s/Plate%s-%s-c2.png' % (file_path, j, i))
        monochrome(im3, 160, 150, 100)
        file3 = np.array(im3)

        print 1
        average_im = (file1 + file2 + file3)/3
        print 2
        misc.imsave('%s/Average_Image_%s_%s.png' % (file_path, j, i), average_im)
        print 'Averaging image %s-%s' % (j, i)


def crop_image(im):
    """cuts individual seeds into image stacks,Cropping areas are set as the grid in image capture."""
    image = Image.open(im)

    dimensions = {1: (195, 30, 501, 371),  # dimensions for cropping of each seed
                  2: (501, 30, 807, 371),  # l, top, r, bottom dimensions
                  3: (807, 30, 1113, 371),
                  4: (1113, 30, 1419, 371),
                  5: (1419, 30, 1725, 371),
                  6: (195, 371, 501, 711),  # row 2
                  7: (501, 371, 807, 711),
                  8: (807, 371, 1113, 711),
                  9: (1113, 371, 1419, 711),
                  10: (1419, 371, 1725, 711),
                  11: (195, 711, 501, 1050),  # row 3
                  12: (501, 711, 807, 1050),
                  13: (807, 711, 1113, 1050),
                  14: (1113, 711, 1419, 1050),
                  15: (1419, 711, 1725, 1050)}

    for keys in dimensions:
        cropped_im = image.crop(dimensions[keys])
        im = im.split('.png')[0]
        cropped_im.save(im + '_crop%s.png' % keys)


def process(image_name):
    """Machine vision processing - image thresholded, filtered and the y coordinate of the center of mass extracted"""
    f = np.array(Image.open(image_name))
    f = inter.rotate(f, 180, axes=(1, 0))  # flips image horizontally so image is read from bottom left perspective
    f = f[:, :, 0]  # applies blue colour scheme
    f = ndimage.filters.gaussian_filter(f, 0.5)
    f = (f > f.mean())
    f = ndimage.binary_opening(f, iterations=2)

    maxim1 = ndimage.center_of_mass(f, labels=None)  # gets the center of mass of thresholded object
    os.remove(image_name)  # removes each cropped image to save disk space
    print 'Processing %s' % image_name
    return maxim1[1]


def analysis_procedure():
    """Links analysis steps together. Firstly images are averaged, then cropped, and finally processed
    individually"""
    try:
        for j in cam_list:  # cycles through each selected camera
            average_images(j)

            for k in range(1, img_nmb):  # cycles through each averaged image.
                crop_image('%s/Average_Image_%s_%s.png' % (file_path, j, k))
                os.remove('%s/Average_Image_%s_%s.png' % (file_path, j, k))  # removes average image

                for l in range(1, 16):  # cycles through each cropped average image
                    maxim = process('%s/Average_Image_%s_%s_crop%s.png' % (file_path, j, k, l))
                    key = 'Plate%s_seedling%s' % (j.zfill(2), str(l).zfill(2))
                    DataDict.setdefault(key, [])  # checks if key exists and if not creates one with empty val
                    DataDict[key].append(maxim)

    except IOError:
        print 'Error - no such files or directory could be found.'


def filter_noise(data):
    """Ignores frames where the center of mass is outside of the mean which would disrupt tracking significantly"""
    for keys in data:  # cycles through each plate in dict
        data2 = data[keys]
        mean = scipy.stats.nanmean(data2)  # calculates mean center of mass of whole stack ignoring blank values
        try:
            for i in data2:  # cycles through each data point for a plate
                indx = data2.index(i)  # if data is outside of mean change to nan
                if [mean + [20]] < i < [mean - [20]]:
                    data2[indx] = np.nan

            datal = np.array(data2)
            ok = -np.isnan(datal)  # interpolates nan values
            xp = ok.ravel().nonzero()[0]
            fp = datal[-np.isnan(data2)]
            x = np.isnan(datal).ravel().nonzero()[0]
            datal[np.isnan(datal)] = np.interp(x, xp, fp)
            data[keys] = datal
        except ValueError:
            pass
		


def export(DataDict):
    """Exports dictionary to csv file"""
    ims = range(1, (img_nmb))  # creates a time column for plotting
    time = [i * time_int for i in ims]  # converts image number into time column
    DataDict['0Time_(hours)'] = time  # adds time as first col in dictionary
    keys = sorted(DataDict.keys())
    with open('%s/Results/Output_%s.csv' % (file_path, file_path), 'wb') as f:
        w = csv.writer(f)
        w.writerow(keys)
        w.writerows(zip(*[DataDict[key] for key in keys]))


def plot(d):
    """Plots the processed data roughly"""
    time = d['0Time_(hours)']  #  gets time for dict
    for k in d:
        data = d[k]  # gets y co-ordinates from dict for y axis
        pyp.plot(time, data)
        pyp.xlim([0, max(time)])
        pyp.xlabel('Time (minutes)')
        pyp.ylabel('Relative pixel position')
        pyp.savefig('%s/Results/%s.png' % (file_path, k))
        pyp.close()

    os.remove('%s/Results/0Time_(hours).png' % file_path)  # removes the time plot


# Collects all user inputs and converts to parameters for analysis.
file_path = raw_input('Specify image directory (%s/):' % os.path.expanduser("~"))  # expanduser sets home directory and works cross-platform
cam_nmb = raw_input('Specify plates used (comma delimited e.g 1,2,5):')
cam_list = cam_nmb.split(',')
img_nmb = int(raw_input('Specify number of images in stack:'))
time_int = raw_input('Specify time interval (seconds):')
time_int = (float(time_int))/3600

# Runs the analysis, does a little quality control, then exports to csv
setup_analysis()
analysis_procedure()
filter_noise(DataDict)
export(DataDict)
#Matplotlib currently wont work with pyinstaller wrapping.
#plot(DataDict)

