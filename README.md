# Accelerating Bayesian Optimization Structure Search with Transfer Learning

Wellcome to BOSS-MT. This repo contains the data analysis scripts used in my 2020 M.Sc. thesis 'Accelerating Bayesian Optimization Structure Search with Transfer Learning'. The purpose of this repository is to allow verifying and reproducing the results of my thesis work. This is not a user manual for using transfer learning with BOSS. See the BOSS project (references in the thesis) for further information on BOSS use.

The folder structure is the following:

- data: Raw experiment data. Scripts for running BOSS experiments, inputs, outputs, molecular simulation scripts etc. Not version controlled. The data is compressed in a tar file (experiments.tgz). To uncompress the raw data, use <code>tar -xvf experiments.tgz<\code>. WARNING: the uncompressed raw data requires 100GB of free disc space!

- processed_data: Raw data (boss.out files) parsed to json format for analysis.

- results: figures and tables created by the analysis scripts are created here.

- src: Analysis scripts and configuration files.

## Understanding the experiments

It is assumed that the user is familiar with the thesis work.
Each folder in data / processed data contains output of one experiment. Each experiment is named with a 4 character code as follows:
![Naming of the experiments](visuals/naming_experiments.png)
Most experiments contain multiple BOSS runs. Each boss run is named exp_N, where N is a running number. The settings in all runs under same experiment are equal, but the number of secondary data, and the initialization data itself, may vary for statistics depending on the experiment.\
Processed data is in json format. You can load data of each run to python dictionary with python json module using <code>json.load(filepath)<\code>.
The setup for each experiment run can be seen from "boss.in" keyword. Relevant settings are also listed under their own keywords. Use <code>.keys()<\code> function to list all the keywords for a setup.

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

## Citing the work
To cite, use:

Sten, N. A. 2020. 'Accelerating Bayesian Optimization Structure Search with Transfer Learning'. M.Sc. Thesis. Aalto University. Espoo, Finland. DOI/URN.\
% save to zenodo https://sandbox.zenodo.org/login/\
or load [bibtex citation](https://github.com/NuuttiSten/BOSS-MT/blob/master/sten2020accelerating.bib).
