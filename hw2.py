from numpy import zeros
from skimage.io import imread, imsave
from skimage.filters.rank import median, threshold
from skimage.filters import threshold_otsu
from skimage.morphology import disk, closing, square
from skimage.exposure import adjust_gamma
from skimage.measure import regionprops, label
from skimage.segmentation import clear_border
from skimage.transform import resize

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import os

def image_prep(img):
	# apply filters for better contrast and noise removal
	img_gamma = adjust_gamma(img, 0.7)
	img_median = median(img_gamma, disk(1))

	# apply threshold
	val =  threshold_otsu(img_median)
	img_otsu = img_median > val

	# label image regions
	label_image = label(img_otsu)

	candidates = []
	for region in regionprops(label_image):
		minr, minc, maxr, maxc = region.bbox
		if (maxr - minr > maxc - minc):
			candidates.append(region)

	# find numbers
	areas = []
	for candidate in candidates:
		areas.append(candidate.area)
	areas.sort()
	areas.reverse()

	n = 1
	v = []
	for candidate in candidates:
		if (candidate.area == areas[0] or candidate.area == areas[1] or candidate.area == areas[2]):
			v.append(candidate.image)
			imsave('num%d.png' % n, candidate.image)
			n += 1
	return v

def generate_template(digit_dir_path):
	i = 1
	listing = os.listdir(digit_dir_path)
	img = imread(digit_dir_path + listing[0])
	for image in listing:
		try:
			newimg = imread(digit_dir_path + image)
			newimg = resize(newimg, img.shape)
			img += newimg
			i += 1
		except:
			pass
	return img//i

def cross(number, template):
	num = resize(number, template.shape)
	acc = 0
	for i in range(num.shape[0]):
		for j in range(num.shape[1]):
			acc += abs(1-num[i][j]-template[i][j])
	return acc/(num.shape[0]*num.shape[1])

def recognize_each(number, templates):
	index = -1
	best = 0
	for i in range(len(templates)):
		temp = cross(number, templates[i])
		if (index == -1 or index >= 0 and temp < best):
			best = temp
			index = i
	return index

def recognize(img, digit_templates):
	listing = os.listdir(digit_templates)
	listing.sort()
	templates = []
	for number in listing:
		templates.append(generate_template(digit_templates + number + '/'))
	nums = image_prep(img)
	l = []
	for num in nums:
		l.append(recognize_each(num, templates))
	return tuple(l) 
