import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import sys
import os

from astropy.modeling import models
from astropy import units as u

from specutils.spectra import Spectrum1D, SpectralRegion
from specutils.fitting import fit_generic_continuum

files = ["v2gammaCas_1.fits",  
"v2gammaCas_2.fits", 
"v2gammaCas_2.fits", 
"v2gammaCas_1.fits", 
"v3gammaCas_1.fits",  
"v3gammaCas_2.fits",  
"v1rhoLeo_1.fits",			
"v1rhoLeo_2.fits",  
"v2rhoLeo_2.fits",  
"v2rhoLeo_1.fits",  
"v3rhoLeo_1.fits",  
"v3rhoLeo_2.fits",  
"v4rhoLeo_2.fits",  
"v4rhoLeo_1.fits",  
"v5rhoLeo_1.fits",  
"v5rhoLeo_2.fits",  
"v6rhoLeo_2.fits",  
"v6rhoLeo_1.fits",  
"v7rhoLeo_1.fits",  
"v7rhoLeo_2.fits",   
"v8rhoLeo_2.fits",  
"v8rhoLeo_1.fits",  
"v9rhoLeo_1.fits",  
"v9rhoLeo_2.fits",  
"v10rhoLeo_2.fits",  
"v10rhoLeo_1.fits",  
"v11rhoLeo_1.fits",  
"v11rhoLeo_2.fits",  
"v12rhoLeo_2.fits",  
"v12rhoLeo_1.fits",  
"v13rhoLeo_1.fits",  
"v13rhoLeo_2.fits",  
"v14rhoLeo_2.fits",  
"v14rhoLeo_1.fits",  
"v15rhoLeo_1.fits",  
"v15rhoLeo_2.fits",  
"v16rhoLeo_2.fits",  
"v16rhoLeo_1.fits",  
"v17rhoLeo_1.fits",  
"v17rhoLeo_2.fits",  
"v18rhoLeo_2.fits",  
"v18rhoLeo_1.fits",  
"v19rhoLeo_1.fits",  
"v19rhoLeo_2.fits",  
"v19rhoLeo_2.fits", 
"v20rhoLeo_2.fits",   
"v20rhoLeo_1.fits",  
"v21rhoLeo_1.fits",  
"v21rhoLeo_2.fits",  
"v22rhoLeo_2.fits",  
"v22rhoLeo_1.fits",  
"v22rhoLeo_1.fits", 
"v23rhoLeo_1.fits", 
"v23rhoLeo_2.fits", 
"v24rhoLeo_2.fits", 
"v24rhoLeo_1.fits", 
"v25rhoLeo_1.fits", 
"v25rhoLeo_2.fits", 
"v26rhoLeo_2.fits", 
"v26rhoLeo_1.fits", 
"v27rhoLeo_1.fits", 
"v27rhoLeo_2.fits", 
"v28rhoLeo_2.fits", 
"v28rhoLeo_1.fits", 
"v29rhoLeo_1.fits", 
"v29rhoLeo_2.fits", 
"v30rhoLeo_2.fits", 
"v30rhoLeo_1.fits", 
"v31rhoLeo_1.fits", 
"v31rhoLeo_2.fits", 
"v32rhoLeo_2.fits", 
"v32rhoLeo_1.fits", 
"v33rhoLeo_1.fits", 
"v33rhoLeo_2.fits", 
"v34rhoLeo_2.fits", 
"v34rhoLeo_1.fits", 
"v35rhoLeo_1.fits", 
"v35rhoLeo_2.fits", 
"v35rhoLeo_1.fits", 
"v36rhoLeo_1.fits", 
"v36rhoLeo_1.fits", 
"v36rhoLeo_2.fits", 
"v37rhoLeo_2.fits", 
"v37rhoLeo_1.fits", 
"v38rhoLeo_1.fits", 
"v38rhoLeo_2.fits", 
"v39rhoLeo_2.fits", 
"v39rhoLeo_1.fits", 
"v40rhoLeo_1.fits", 
"v40rhoLeo_2.fits", 
"vHD33256_1.fits", 
"vHD33256_2.fits", 
"vHD137916_1.fits", 
"vHD137916_2.fits", 
"vHD200405_1.fits", 
"vHD200405_2.fits", 
"vHD201601_1.fits", 
"vHD201601_2.fits", 
"vHD290665_2.fits", 
"vHD290665_1.fits",]

# np.random.seed(0)
# x = np.linspace(0., 10., 200)
# y = 3 * np.exp(-0.5 * (x - 6.3)**2 / 0.1**2)
# y += np.random.normal(0., 0.2, x.shape)

# y_continuum = 3.2 * np.exp(-0.5 * (x - 5.6)**2 / 4.8**2)
# y += y_continuum
if __name__ == "__main__":
	# Get the filename of the spectrum from the command line, and plot it
	for filename in files:
		opened_file = fits.open(filename)
		hdu = opened_file[0]
		data = hdu.data
		xSize = data.shape[0]
		x = range(xSize)
		y = data

		spectrum = Spectrum1D(flux=y*u.Jy, spectral_axis=x*u.um)
		g1_fit = fit_generic_continuum(spectrum)
		y_continuum_fitted = g1_fit(x*u.um)
		spec_normalized = spectrum / y_continuum_fitted

		hdu.data = spec_normalized.flux.value
		# hdu.header['CRVAL1'] = hdu.header['CRVAL1'] + diffX * hdu.header['CDELT1']
		if os.path.exists('./autonorm/norm_' + filename):
			os.remove('./autonorm/norm_' + filename)
		hdu.writeto('./autonorm/norm_' + filename)
		opened_file.close()
		# plt.close('all')

		# plt.plot(spec_normalized.spectral_axis, spec_normalized.flux)
		# plt.title('Continuum normalized spectrum')
		# plt.grid('on')
		# plt.show()

