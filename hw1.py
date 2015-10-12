from numpy import array, dstack, roll
from skimage.transform import rescale

def MSE(I1, I2):
	I1 = I1.astype('float64')
	I2 = I2.astype('float64')
	diff = (I1 - I2).flatten()
	return diff.dot(diff)/float(I1.shape[0]*I1.shape[1])

def coveredMSE(I1, I2, i, j):
	height = I1.shape[0]
	width = I1.shape[1]
	if (i < 0):
		if (j > 0):
			return MSE(I1[:height-i, j:], I2[:height-i, j:])
		else:
			return MSE(I1[:height-i, :width-j], I2[:height-i, :width-j])
	elif (j > 0):
		return MSE(I1[i:, j:], I2[i:, j:])
	else:
		return MSE(I1[i:, :width-j], I2[i:, :width-j])

def findBestRoll(I1, I2, rangei, rangej):
	bestMSERoll= [0, 0]
	bestMSE = MSE(I1, I2)
	for i in rangei:
		for j in rangej:
			iterMSE = coveredMSE(roll(roll(I1, j, 1), i, 0), I2, i, j)
			if (iterMSE < bestMSE):
				 bestMSE, bestMSERoll = iterMSE, [i, j]
	return bestMSERoll

def pyramid(I1, I2):
	if (I1.shape[0]<=500 and I1.shape[1]<=500):
		return findBestRoll(I1, I2, range(-15, 15), range(-15, 15))
	else:
		I1R = rescale(I1, 0.5)
		I2R = rescale(I2, 0.5)
		rangeValues = pyramid(I1R, I2R)
		print(rangeValues)
		return findBestRoll(I1, I2, range(rangeValues[0]*2-2, rangeValues[0]*2+3), range(rangeValues[1]*2-2, rangeValues[1]*2+3))

def align(bgr_image):
	top = bgr_image[:height, :]
	top = top[height*5//100:height*95//100, \
	width*5//100:width*95//100]

	middle = bgr_image[height:height*2, :]
	middle = middle[height*5//100:height*95//100, \
	width*5//100:width*95//100]

	bottom = bgr_image[height*2:height*3, :]
	bottom = bottom[height*5//100:height*95//100, \
	width*5//100:width*95//100]

	pRoll1 = pyramid(top, middle)
	pRoll2 = pyramid(bottom, middle)
	bgr_image = dstack([roll(roll(bottom, pRoll2[0], 0), pRoll2[1], 1), middle, roll(roll(top, pRoll1[0], 0), pRoll1[1], 1)])
	return bgr_image
