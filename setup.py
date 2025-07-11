import setuptools

setuptools.setup(
	name = "gaiacmds",
	version = "0.5",
	author = "Ava Polzin",
	author_email = "apolzin@uchicago.edu",
	description = "Good enough CMDs based on simple star cluster member selection.",
	packages = ["gaiacmds"],
	url = "https://github.com/avapolzin/goodenough_gaia_cmds",
	license = "MIT",
	classifiers = [
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Programming Language :: Python"],
	python_requires = ">=3",
	install_requires = ["astropy", "astroquery", "matplotlib", "numpy", "pandas"]
)