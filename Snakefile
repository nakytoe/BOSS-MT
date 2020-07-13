

# Preprocess data

EXP_RAW_FOLDER = glob_wildcards('data/{exp_name}/')
EXP_RAW_BOSSOUT = glob_wildcards(join(EXPERIMENT_FOLDER, 'exp_{exp_num}/boss.out'))

rule all:
    input:
        filename = EXP_RAW_BOSSOUT
    shell:
        'echo {input.filename}'