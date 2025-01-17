#!/usr/bin/env python

"""Batch process all images of compound eyes and save data.


Assumes the following folder structure:

.\
|--batch_process_images.py
|--pixel_size.csv (optional)    # stored pixel-to-distance conv.
|--image_001.jpg
|--image_002.jpg
|...
|--masks\
   |--image_001.jpg             # white sillouetting mask on black background
   |--image_002.jpg
   |...
|--image_001_ommatidia.jpg (outcome)
|--image_002_ommatidia.jpg (outcome)
|...
|--ommatidia_data.csv
|--_hidden_file
"""
import os
from scipy import misc
import sys 
# sys.path.append("H://My Drive//backup//Desktop//programs//ODA//ODA//src//ODA")
# from analysis_tools import *
from ODA import *
import pandas as pd


# Custom parameters
# if a list, must be one-to-one with images
BRIGHT_PEAK = False             # True assumes a bright point for every peak
HIGH_PASS = True               # True adds a high-pass filter to the low-pass used in the ODA
SQUARE_LATTICE = True          # True assumes only two fundamental gratings
FILE_EXTENSION = ".tif"        # assumes you're only interested in this file extension


# make dictionary to store relevant information
values = {
    "filename":[], "eye_area":[], "eye_length":[], "eye_width":[],
    "ommatidia_count":[], "ommatidial_diameter":[], "ommatidial_diameter_SD":[],
    "ommatidial_diameter_fft":[]
}

# load filenames and folders
fns = os.listdir(os.getcwd())
img_fns = [fn for fn in fns if fn.endswith(FILE_EXTENSION)]
img_fns = [fn for fn in img_fns if "ommatidia" not in fn] # omit outcome images
folders = [fn for fn in fns if os.path.isdir(fn)]
folders = [os.path.join(os.getcwd(), f) for f in folders]
# load the mask filenames
mask_fns = os.listdir("./masks")
mask_fns = [os.path.join(os.getcwd(), "masks", f) for f in mask_fns]
mask_fns = [fn for fn in mask_fns if fn.endswith(FILE_EXTENSION)]
# load pixel sizes from a local file, if present
pixel_sizes = []
if os.path.exists("pixel_size.csv"):
    pixel_sizes_csv = pd.read_csv("pixel_size.csv")
    for img_fn in img_fns:
        breakpoint()
else:
    PIXEL_SIZE=1
# for each image
for img_fn in img_fns:
    # find mask file with same filename
    ind = [img_fn in fn for fn in mask_fns]
    if sum(ind) == 1:
        mask_fn = mask_fns[np.where(ind)[0][0]]
        # skip hidden files
        if not img_fn.startswith("_"):
            print(img_fn)
            # get new filename from the image filename
            fn_base = img_fn.split(".")[0]
            result_fn = f"{fn_base}_ommatidia.jpg"
            # generate the Eye object using the image
            eye = Eye(img_fn, bw=True, mask_fn=mask_fn)
            eye.oda(bright_peak=BRIGHT_PEAK, high_pass=HIGH_PASS, square_lattice=SQUARE_LATTICE, plot_fn=result_fn, manual_edit=False, regular=True)
            # store relevant parameters
            for key in values.keys():
                if key in dir(eye):
                    values[key] += [getattr(eye, key)]
                elif key == 'ommatidia_count':
                    values[key] += [len(eye.ommatidial_inds)]
            print()

dataframe = pd.DataFrame(values)
dataframe.to_csv("eye_data.csv", index=False)

