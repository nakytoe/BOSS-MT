

EXP_wildcard = glob_wildcards('data/experiments/{exp_name}/boss.out')
EXP_NAME = EXP_wildcard.exp_name

rule parse_raw_bossout:
    input:
        expand('data/experiments/{exp_name}/boss.out',
                exp_name = EXP_NAME)
    output:
        expand('processed_data/{exp_name}.json',
                exp_name = EXP_NAME)
    run:
        for infile, expname, outfile in zip(input, EXP_NAME, output):
            name = '_'.join(expname.split('/exp_'))
            line = f'python3 src/parse/parse_BOSS_output.py {infile} {name} {outfile}'
            shell(line)