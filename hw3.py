import numpy as np
from math import atan2
from scipy.ndimage import convolve
from scipy.misc import imsave
from skimage.io import imread, imsave
from skimage.color import rgb2gray

def extract_hog(img):
	img = rgb2gray(img)

	#computing convolution
	Ix = convolve(img, [[-1, 0, 1]])
	Iy = convolve(img, [[-1], [0], [1]])

	#gradient
	grad = np.sqrt(np.power(Ix, 2)+np.power(Iy, 2))
	Ig = np.ndarray((Ix.shape[0], Ix.shape[1]))
	for i in range(Ig.shape[0]):
		for j in range(Ig.shape[1]):
			Ig[i][j] = atan2(Ix[i][j], Iy[i][j])

	#divide into cells and compute histogram
	cellRows = 3
	cellCols = 3
	nRows = Ig.shape[0]//cellRows
	nCols = Ig.shape[1]//cellCols
	hist_of_cells = []
	binCount = 9
	for i in range(nRows):
		hist_of_cells.append([])
		for j in range(nCols):
			hist_of_cells[i].append(np.histogram(Ig[i:i+cellRows-1, j:j+cellCols-1], bins=binCount, \
				weights=grad[i:i+cellRows-1, j:j+cellCols-1]))

	#cells into blocks, concatenate histograms
	blockRowCells = 2;
	blockColCells = 2;
	nBlockRows = nRows//blockRowCells
	nBlockCols = nCols//blockColCells
	conc_hist_blocks = []
	for i in range(nBlockRows):
		conc_hist_blocks.append([])
		for j in range(nBlockCols):
			print(hist_of_cells[i:i+blockRowCells-1][j:j+blockColCells-1])

img = imread("img.png")
extract_hog(img)
