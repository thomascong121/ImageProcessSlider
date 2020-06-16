import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import Slider, Button, RadioButtons
#slider: threshold, kernelsize, std for gaussian filtering
#button: 1. smoothing: median/gaussian 2. filtering: global/otsu/adaptive mean/gaussian
class my_Slider:
	def __init__(self, img, threshold = 30, kernel = 5, std = 5):
		self.img = img
		self.threshold = threshold
		self.smooth = 'Gaussian smooth'
		self.k = kernel
		self.s = std
		self.fig = plt.figure()
		self.p  = self.draw_plots(self.img, self.threshold, self.smooth, self.s)
		#set up sliders - location
		axcolor = 'lightgoldenrodyellow'
		ax_threshold = self.fig.add_axes([0.25, 0.01, 0.65, 0.02], facecolor=axcolor)
		ax_kernel = self.fig.add_axes([0.25, 0.03, 0.65, 0.02], facecolor=axcolor)
		ax_std = self.fig.add_axes([0.25, 0.05, 0.65, 0.02], facecolor=axcolor)
		#set up sliders - content, length, width
		self.s_threshold = Slider(ax_threshold, 'Threshold', 0.0, 255.0, valinit = 30.0, valstep = 10.0)
		self.s_kenel = Slider(ax_kernel, 'Kernel', 3.0, 21.0,valinit = 5.0, valstep = 2.0)
		self.s_std = Slider(ax_std, 'Std', 1.0, 15.0, valinit = 5.0, valstep = 2.0)
		#set up buttons
		resetax = self.fig.add_axes([0.01, 0.025, 0.1, 0.04])
		self.button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
		rax = self.fig.add_axes([0.01, 0.5, 0.25, 0.25], facecolor=axcolor)
		self.radio = RadioButtons(rax, ('Gaussian smooth', 'median smooth'), active=0)

		self.s_threshold.on_changed(self.update)
		self.s_kenel.on_changed(self.update)
		self.s_std.on_changed(self.update)

		self.button.on_clicked(self.reset)
		self.radio.on_clicked(self.buttonfunc)

		self.p.show()

	def draw_plots(self, img, threshold_value, smooth, kernel = 11, std = 1, C=2,  maxVal=255, onplot = None):
		threshold_value = int(threshold_value)
		kernel = int(kernel)
		img = cv2.imread(img,0)

		if smooth == 'median smooth':
			img= cv2.medianBlur(img,kernel)
		elif smooth == 'Gaussian smooth':
			img= cv2.GaussianBlur(img,(kernel,kernel),std)

		#global
		ret , thresh1 = cv2.threshold(img,threshold_value,maxVal,cv2.THRESH_BINARY)

		#otsu
		ret2, thresh2 = cv2.threshold(img,0,maxVal,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

		#adaptive
		thresh3 = cv2.adaptiveThreshold(img,maxVal,cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY,kernel,C)
		thresh4 = cv2.adaptiveThreshold(img,maxVal,cv2.ADAPTIVE_THRESH_GAUSSIAN_C , cv2.THRESH_BINARY,kernel,C)
		titles = ['Binary','Otsu','Adaptive-mean','Adaptive-gaussian','histogram']
		images = [thresh1,thresh2,thresh3,thresh4]
		nrow = 2
		ncol = 2

		for i in range(4):
			self.fig.add_subplot(2,2,i+1)
			plt.imshow(images[i],'gray')
			plt.title(titles[i],fontsize=8)
			plt.xticks([]),plt.yticks([])
			plt.tight_layout() 
			plt.subplots_adjust(left=0.25,bottom=0.1,top=0.9,right=0.95,hspace=0.1,wspace=0)
		return plt

	def update(self, val):
		self.threshold = int(self.s_threshold.val)
		self.k = int(self.s_kenel.val)
		self.s = int(self.s_std.val)

		p = self.draw_plots(self.img, self.threshold, self.smooth, kernel = self.k, std = self.s)
		p.show()
		self.fig.canvas.draw_idle()

	
	def reset(self, event):
		self.s_threshold.reset()
		self.s_kenel.reset()
		self.s_std.reset()

	def buttonfunc(self, label):
		self.smooth = label
		p2 = self.draw_plots(self.img, self.threshold, self.smooth, kernel = self.k, std = self.s)
		p2.show()
		self.fig.canvas.draw_idle()
	


if __name__ == '__main__':
	img_path = input('Input image path:')
	s = my_Slider(img_path)