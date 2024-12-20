def refine_salary(salary_estimates_raw):
    import pandas as pd
    import numpy as np

    relative_level_yoe_mapping = pd.read_csv('data/reference/relative_level_yoe_mapping.csv')
    relative_role_mapping = pd.read_csv('data/reference/relative_role_mapping.csv')
    relative_country_mapping = pd.read_csv('data/reference/relative_country_mapping.csv')
    
    se_ss = salary_estimates_raw.copy()

    global_median = np.median(se_ss['M'])

    level_mod_est = relative_level_yoe_mapping.merge(
                    se_ss.groupby(['yoe', 'level'])['M'].agg('median').reset_index(), 
                    on = ['yoe', 'level'], how = 'left')
    level_mod_est['actual_per_diff'] = (level_mod_est['M'] - global_median) / global_median
    level_mod_est['mod_perc_level_macro'] = 1 + (level_mod_est['level_per_diff'] - level_mod_est['actual_per_diff'])
    level_mod_est = level_mod_est[['yoe', 'level', 'mod_perc_level_macro']]
    se_ss = se_ss.merge(level_mod_est, on = ['yoe', 'level'], how = 'left')

    se_ss = se_ss.merge(relative_level_yoe_mapping, on = ['yoe', 'level'], how = 'left')
    
    se_ss['actual_per_diff'] = (se_ss['M'] - global_median) / global_median

    se_ss['mod_perc_level_micro'] = 1 + (se_ss['level_per_diff'] - se_ss['actual_per_diff'])
    
    se_ss['mean_per_adjust'] = (se_ss['mod_perc_level_macro'] + se_ss['mod_perc_level_micro']) / 2

    se_ss['M_adjusted'] = se_ss['mean_per_adjust'] * se_ss['M']
    
    return(se_ss)
