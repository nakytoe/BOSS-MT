# Transfer learning experiments

Each experiment contains all inputs, outputs and utilities of that run. 

## Some terminology
HF: high fidelity density functional theory (dft) experiments,
    primary BOSS task is the PES estimate of Friz-Haber ab ignitio molecular simulations (FHI-aims) 
LF: low fidelity force field (AMBER) experiments,
    primary BOSS task is the PES estimate of AMBERtools18

## The basic experiment structure is the following:
Each experiment folder contains a baseline run, where BOSS is laos-boats 0.9.17. The baseline is stored inside 'baseline' folder.

Then there are experiments, which are typically named exp_number. These experiments are very similar to each other, and have some variable(s) that change between experiments. Experiments were run as an array job using the script in run_array.sh
The experiments are run with multi-output  modification of laos-boats 0.9.17 that has trandfer learning. This code has not yet been published.

There is also a 'job' folder that stores stderror and stdout from array run.

For each experiments check the scripts for exact setup information. 
