# `gaiacmds`
*Good enough* automatic cluster membership selection to recover CMDs for use in the classroom!


## Installation
To install:

```bash
cd ~

git clone https://github.com/avapolzin/goodenough_gaia_cmds.git

cd gaiacmds

pip install .

````
or 
```bash
pip install gaiacmds
```

## Getting Started
import gaiacmds

This code is designed to auto-generate CMDs from Gaia data based on a simple object name search. While not using a sophisiticated selection function suited to *research* purposes, results are good enough for pedagogical use, including explaining SSPs (or CSPs as the case may be), fitting isochrones, and recovering age/distance/metallicity for open and globular clusters.

`gaiacmds` ships with easy plotting functions for MIST and PARSEC stellar isochrones for Gaia EDR3. BaSTI may be added in the future.

Stellar isochrone models will not always perfectly align with CMD, and, for example, [this paper](https://arxiv.org/abs/2411.12987) may be of interest in understanding discrepancies between the CMD and theoretical isochrone positions. Additionally, for consistency between models, all of the synthetic *Gaia* photometry is for EDR3, and all models use solar abundance patterns.


autodist for parallax distance
is feh also in Gaia?

Will create two types of functions -- one quickplot (show CMD, opt into isochrones), one that acts as plotting function to be placed in fig = plt.figure object.