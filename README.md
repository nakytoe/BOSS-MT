# BOSS-MT - Accelerating Bayesian Optimization Structure Search with Transfer Learning

Wellcome to BOSS-MT. This folder contains the data and scripts used in my thesis 'Accelerating Bayesian Optimization Structure Search with Transfer Learning'.

The folder structure is the following:

- data/: Raw experiment data. Scripts for running BOSS experiments, inputs, outputs, molecular simulation scripts etc.

- processed_data/: Data parsed from experiments for analytics.

- results/: Graphs and tables produces in the analysis.

- src:/ Analysis scripts and config files.

- doc/: The thesis.

- demo/: Demo notebooks.

## Reproducing the analysis

The analysis pipelines in this project are managed by [Snakemake](https://snakemake.readthedocs.io/en/stable/).
All the analysis is completely reproducible. The main input file for running the analysis is Snakefile, that can be found here in the root folder.
To run the analysis, copy clone this repository\
<code>git clone </code>\
install [anaconda](https://www.anaconda.com) virtual environment with the [requirements](https://github.com/NuuttiSten/BOSS-MT/blob/master/requirements.txt)\
<code>conda create --name stenthesis --file requirements.txt </code>,
launch the environment\
<code>conda activate stenthesis></code>\
and run Snakemake with\
<code>snakemake</code>.\
Parsed data is saved under <code>processed_data/</code>.\
Final analysis outputs are stored to <code>results/</code>.\
To clean all outputs, run\
<code>snakemake --delete-all-output</code>.

Special Gotchas of your projects (Problems you faced, unique elements of your project)
Technical Description of your project like- Installation, Setup, How to contribute.\

To cite, use\

Sten, N. A. 2020. 'Accelerating Bayesian Optimization Structure Search with Transfer Learning'. M.Sc. Thesis. Aalto University. Espoo, Finland. DOI/URN.\
% save to zenodo https://sandbox.zenodo.org/login/\
or load [bibtex citation](https://github.com/NuuttiSten/BOSS-MT/blob/master/sten2020accelerating.bib).
