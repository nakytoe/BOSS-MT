

EXP_wildcard = glob_wildcards('data/experiments/{exp_name}/boss.out')
EXP_NAME = EXP_wildcard.exp_name
print(EXP_NAME)

rule somerule:
    input:
        expand('data/experiments/{exp_name}/boss.out',
                exp_name = EXP_NAME)
    output:
        'processed_data/'.join(,input.split('/')[0],'_', input.split['_'][-1])