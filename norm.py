import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splrep,splev
import sys
import os
from astropy.io import fits


def onclick(event):
	# when none of the toolbar buttons is activated and the user clicks in the
	# plot somewhere, compute the median value of the spectrum in a 10angstrom
	# window around the x-coordinate of the clicked point. The y coordinate
	# of the clicked point is not important. Make sure the continuum points
	# `feel` it when it gets clicked, set the `feel-radius` (picker) to 5 points
	toolbar = plt.get_current_fig_manager().toolbar
	if event.button==1 and toolbar.mode=='' and cur_mode=="pre_n":
		window = ((event.xdata-5)<=wave) & (wave<=(event.xdata+5))
		y = np.median(flux[window])
		plt.plot(event.xdata,y,'rs',ms=4,picker=5,label='cont_pnt')
	if event.button==1 and toolbar.mode=='' and cur_mode=="post_n":
		window = ((event.xdata-5)<=wave) & (wave<=(event.xdata+5))
		y = 1
		plt.plot(event.xdata,y,'rs',ms=4,picker=5,label='cut_pnt')
	plt.draw()

def onpick(event):
	# when the user clicks right on a continuum point, remove it
	if event.mouseevent.button==3:
		if hasattr(event.artist,'get_label') and (event.artist.get_label()=='cont_pnt' or event.artist.get_label()=='cut_pnt'):
			event.artist.remove()

def ontype(event):
	global cur_mode
	global normalised
	global wave
	global diffX
	# when the user hits enter:
	# 1. Cycle through the artists in the current axes. If it is a continuum
	#	point, remember its coordinates. If it is the fitted continuum from the
	#	previous step, remove it
	# 2. sort the continuum-point-array according to the x-values
	# 3. fit a spline and evaluate it in the wavelength points
	# 4. plot the continuum
	if event.key=='enter':
		cont_pnt_coord = []
		for artist in plt.gca().get_children():
			if hasattr(artist,'get_label') and artist.get_label()=='cont_pnt':
				cont_pnt_coord.append(artist.get_data())
			elif hasattr(artist,'get_label') and artist.get_label()=='continuum':
				artist.remove()
		cont_pnt_coord = np.array(cont_pnt_coord)[...,0]
		sort_array = np.argsort(cont_pnt_coord[:,0])
		x,y = cont_pnt_coord[sort_array].T
		spline = splrep(x,y,k=3)
		continuum = splev(wave,spline)
		plt.plot(wave,continuum,'r-',lw=2,label='continuum')

	# when the user hits 'n' and a spline-continuum is fitted, normalise the
	# spectrum
	elif event.key=='n':
		continuum = None
		for artist in plt.gca().get_children():
			if hasattr(artist,'get_label') and artist.get_label()=='continuum':
				continuum = artist.get_data()[1]
				break
		if continuum is not None:
			cur_mode = "post_n"
			normalised = flux/continuum
			plt.cla()
			plt.plot(wave,flux/continuum,'k-',label='normalised')
			plt.plot(wave,[1]*len(wave),'k-',label='line1',color="green")

	# when the user hits 'r': clear the axes and plot the original spectrum
	elif event.key=='r':
		cur_mode = "pre_n"
		plt.cla()
		plt.plot(wave,flux,'k-')

	elif event.key=='c':
		cut_pnt_coord = []
		for artist in plt.gca().get_children():
			if hasattr(artist,'get_label') and artist.get_label()=='cut_pnt':
				cut_pnt_coord.append(artist.get_data())
		cut_pnt_coord = np.array(cut_pnt_coord)[...,0]
		sort_array = np.argsort(cut_pnt_coord[:,0])
		x,y = cut_pnt_coord[sort_array].T
		for w in wave:
			if w >= x[0]:
				normalised = normalised[wave.index(w):]
				diffX = wave.index(w)
				wave = wave[wave.index(w):]
				break
		for w in wave:
			if w >= x[1]:
				normalised = normalised[:wave.index(w)]
				wave = wave[:wave.index(w)]
				break
		plt.cla()
		plt.plot(wave,normalised,'k-',label='normalised')
		plt.plot(wave,[1]*len(wave),'k-',label='line1',color="green")


	# when the user hits 'w': if the normalised spectrum exists, write it to a
	# file.
	elif event.key=='w':
		hdu.data = normalised
		hdu.header['CRVAL1'] = hdu.header['CRVAL1'] + diffX * hdu.header['CDELT1']
		if os.path.exists('norm_' + filename):
			os.remove('norm_' + filename)
		hdu.writeto('norm_' + filename)
		plt.close('all')

		# for artist in plt.gca().get_children():
		# 	if hasattr(artist,'get_label') and artist.get_label()=='normalised':
		# 		data = np.array(artist.get_data())
		# 		np.savetxt(os.path.splitext(filename)[0]+'.nspec',data.T)
		# 		print('Saved to file')
		# 		break
	plt.draw()


if __name__ == "__main__":
	# Get the filename of the spectrum from the command line, and plot it
	filename = sys.argv[1]
	# wave,flux = np.loadtxt(filename).T
	# os.system('cp ' + filename + ' norm_' + filename)
	hdu = fits.open(filename)[0]
	data = hdu.data
	xSize = data.shape[0]
	wave = range(xSize)
	flux = data
	spectrum, = plt.plot(wave,flux,'k-',label='spectrum')
	plt.title(filename)
	cur_mode = "pre_n"
	normalised = np.zeros(len(flux))
	diffX = 0

	# Connect the different functions to the different events
	plt.gcf().canvas.mpl_connect('key_press_event',ontype)
	plt.gcf().canvas.mpl_connect('button_press_event',onclick)
	plt.gcf().canvas.mpl_connect('pick_event',onpick)
	plt.get_current_fig_manager().window.showMaximized()
	plt.show() # show the window