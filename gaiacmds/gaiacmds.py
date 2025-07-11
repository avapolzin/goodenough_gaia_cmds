from astropy.coordinates import SkyCoord, name_resolve
import astropy.units as u
from astroquery.gaia import Gaia
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
Gaia.ROW_LIMIT = 2000 #could be set higher for async searches, but probably doesn't need to be

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# #########
#  * * * * 
# #########

def objloc(obj):
	"""
	Get object location.

	Parameters:
		obj (str): Name or coordinates for object of interest. If coordinates, should be in
			HH:MM:SS DD:MM:SS or degree formats. Names must be resolvable in SIMBAD.
	Returns:
		coords (astropy coordinates object)
	"""
	isname = False #check if obj is name or coordinates
	for s in obj:
		if s.isalpha():
			isname = True
			break

	if isname:
		coords = name_resolve.get_icrs_coordinates(obj)

	if not isname:
		if ':' in obj:
			coords = SkyCoord(obj, unit = (u.hour, u.deg), frame = 'icrs')
		if not ':' in obj:
			coords = SkyCoord(obj, unit = u.deg, frame = 'icrs')

	return coords


def select(obj, aper):
	"""
	Select stars from Gaia to include in CMD.

	Parameters:
		obj (str): Name or coordinates for object of interest. If coordinates, should be in
			HH:MM:SS DD:MM:SS or degree formats. Names must be resolvable in SIMBAD.
		aper (float): Radius of cone for cone search in arcmin. 

	Returns:
		Catalog of Gaia stars.
	"""

	cs = Gaia.cone_search_async(objloc(obj), radius=u.Quantity(aper, u.arcmin))
	tab = cs.get_results()
	# keep only values that have photometry
	tab = tab.loc[np.isfinite(tab['phot_bp_mean_mag']) & np.isfinite(tab['phot_rp_mean_mag']) & np.isfinite(tab['phot_g_mean_mag']) ]



def isochrone(logage, feh, dist = 10., blue = 'bp', red = 'rp', mag = 'rp', isos = 'mist'):
	"""
	Return MIST or Parsec synthetic photometry for Gaia EDR3.

	Parameters:
		logage (float): Log age/yrs of isochrone.
		feh (float): [Fe/H] of isochrone.
		dist (float): Distance in parsecs.
		blue (str): 'bp' or 'g'; blue band for color
		red (str): 'g' or 'rp'; red band for color
		mag (str): 'bp', 'g', or 'rp', band to use for magnitude in CMD.
		isos (str): 'mist' or 'parsec'; model isochrones to use.

	Returns:
		color, magnitude
	"""
	url_base = 'https://github.com/avapolzin/goodenough_gaia_cmds/blob/main/isos/%s_gaia_edr3.txt'%isos.lower()
	if isos.lower() in ['mist', 'parsec']:
		iso = pd.read_csv(url_base, sep = ',', header = 0)

	ages = np.sort(np.unique(iso['logage'].values))
	mets = np.sort(np.unique(iso['feh'].values))

	## not interpolating, so grabbing isochrones with *nearest* properties
	near_age = ages[np.argmin(abs(ages - logage))]
	near_met = mets[np.argmin(abs(mets - feh))]

	near_iso = iso.loc[(iso['logage'] == near_age) & (iso['feh'] == near_met)]

	color = near_iso[blue.lower()] - near_iso[red.lower()]
	magn = near_iso[mag.lower()] + 5*np.log10(dist/10) #adjust to apparent magnitude if distance specified

	print('Closest match in %s: log age/yr = %.2f, [Fe/H] = %.2f'%(isos.upper(), near_age, near_met))

	return color, magn


def plot(obj, aper, isos = None, logage = None, feh = None, dist = 10., blue = 'bp', 
			red = 'rp', mag = 'rp'):
	"""
	Plot CMD of stars within cone of specified obj. If isos, will overplot isochrones with stated parameters.

	Parameters:
		obj (str): Name or coordinates for object of interest. If coordinates, should be in
			HH:MM:SS DD:MM:SS or degree formats. Names must be resolvable in SIMBAD.
		aper (float): Radius of cone for cone search in arcmin. 
		isos (str): None, 'mist', or 'parsec'; model isochrones to use. If None, will not plot isochrone.
		logage (float): Log age/yrs of isochrone.
		feh (float): [Fe/H] of isochrone.
		dist (float): Distance in parsecs.
		blue (str): 'bp' or 'g'; blue band for color
		red (str): 'g' or 'rp'; red band for color
		mag (str): 'bp', 'g', or 'rp', band to use for magnitude in CMD.

	Returns:
		Plot showing CMD for stars within cone of specified obj, and, if isos, will overplot isochrone.
	"""

	dat = select(obj, aper)
	cind = '%s_%s'%(blue, red)
	mind = 'phot_%s_mean_mag'%mag

	fig = plt.figure(figsize = (5, 5))
	plt.scatter(dat[cind], dat[mind], color = 'k')

	if isos:
		if None in [logage, feh]:
			raise ValueError('If isos, logage and feh must be provided.')

		iso = isochrone(logage, feh, dist, blue, red, mag)
		plt.plot(iso[0], iso[1], color = 'mediumvioletred')

	plt.title(obj)
	plt.gca().invert_yaxis()
	plt.ylabel(mag)
	plt.xlabel('%s - %s'%(blue, red))
	plt.show()




