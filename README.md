# Description
This is to match ROOT Trees outputted from the ReactionFilter to PSFluxTree files then calculate the total flux from the those files.

# Quick Run Guide
First find the top directory that contains all the files from the ReactionFilter and the tree_PSFlux. In the settings.config paste the directory for the output from the reaction filter in the INPUT_TOPDIR option. Then paste the directory for the tree_PSFlux in the FLUX_DIR option (you probably won't need to change this unless you have custom PSFlux trees. Then type the range in below starting with the first run number and then the last run number.

Then to run: python get_flux_vals.py

# DO NOT MIX EMPTY AND FULL RUNS