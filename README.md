# Accelerating Bayesian Optimization Structure Search with Transfer Learning

Wellcome to BOSS-MT. This repo contains the data analysis scripts used in my 2020 M.Sc. thesis 'Accelerating Bayesian Optimization Structure Search with Transfer Learning'.

The folder structure is the following:

- data: Raw experiment data. Scripts for running BOSS experiments, inputs, outputs, molecular simulation scripts etc. Not version controlled.

- processed_data: The raw data will be parsed here in json format for analysis.

- results: figures and tables created by the analysis scripts are created here.

- src: Analysis scripts and configuration files.

- doc: The thesis.

- demo: Demo notebooks.

## Reproducing the analysis

The analysis pipelines in this project are managed by [Snakemake](https://snakemake.readthedocs.io/en/stable/).
All the analysis is completely reproducible. The main input file for running the analysis is the Snakefile, that can be found here in the root folder.
To run the analysis pipeline, copy clone this repository\
<code>git clone git@github.com:NuuttiSten/BOSS-MT.git</code>\
install [anaconda](https://www.anaconda.com) virtual environment with the [requirements](https://github.com/NuuttiSten/BOSS-MT/blob/master/requirements.txt)\
<code>conda create --name stenthesis --file requirements.txt </code>,\
launch the environment\
<code>conda activate stenthesis></code>\
and run Snakemake with\
<code>snakemake</code>.\
Parsed data is saved under <code>processed_data/</code>.\
Final analysis outputs are stored to <code>results/</code>.\
To clean all outputs, run\
<code>snakemake --delete-all-output</code>.
Parsing the data and running the analysis takes about 15 minutes.

To cite, use:

Sten, N. A. 2020. 'Accelerating Bayesian Optimization Structure Search with Transfer Learning'. M.Sc. Thesis. Aalto University. Espoo, Finland. DOI/URN.\
% save to zenodo https://sandbox.zenodo.org/login/\
or load [bibtex citation](https://github.com/NuuttiSten/BOSS-MT/blob/master/sten2020accelerating.bib).
