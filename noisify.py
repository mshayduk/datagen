import sys
from skimage import io, util, filters
#import numpy as np
import random
from random import uniform, randint



def process_image(mean, var, psf, salt, fimage, fimageout):
    img = io.imread(fimage)
    imgnoisy = util.random_noise(image=img, mode='gaussian',  seed=None, clip=True, mean=mean, var=var)
    imblurred = filters.gaussian(image=imgnoisy, sigma=psf)
    imsalted = util.random_noise(imblurred, mode='salt', amount=salt)
    io.imsave(fimageout, imsalted)
    write_metadata([fimageout, var, psf, salt])    


def write_metadata(fdata):
    with open(fdata[0] + ".meta", 'w') as f:
        f.write("# ********************************************************************** \n")
        f.write("#  input parameters for noisify.py for data: " + fdata[0] + " \n")
        f.write("# ********************************************************************** \n \n ")
        f.write("       fname: " + fdata[0] + "\n")
        f.write("scanner_sigma: " + str(fdata[1]) + "\n")
        f.write("  scanner_psf: " + str(fdata[2]) + "\n")
        f.write(" scanner_salt: " + str(fdata[3]) + "\n \n")


scanner_noises = [0.01, 0.02, 0.025]
scanner_psfs = [1.25/2.35, 1.45/2.35, 1.65/2.35] # 1-D FWHM/2.35 in pixels
scanner_salts = [0.01, 0.02, 0.04]

psf = random.choice(scanner_psfs)
var = random.choice(scanner_noises)
salt = random.choice(scanner_salts)

process_image(mean=0, var=var, psf=psf, salt=salt, fimage=sys.argv[2], fimageout=sys.argv[2])


