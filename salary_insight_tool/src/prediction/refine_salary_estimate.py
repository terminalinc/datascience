def refine_salary(salary_estimates_raw):
    import pandas as pd
    import numpy as np

    relative_level_yoe_mapping = pd.read_csv('data/reference/relative_level_yoe_mapping.csv')
    relative_role_mapping = pd.read_csv('data/reference/relative_role_mapping.csv')
    relative_country_mapping = pd.read_csv('data/reference/relative_country_mapping.csv')
    relative_emptype_mapping = pd.read_csv('data/reference/relative_emptype_mapping.csv')
    
    se_ss = salary_estimates_raw.copy()
    global_median = np.median(se_ss['M'])

    se_ss = se_ss.merge(relative_level_yoe_mapping, on = ['yoe', 'level'], how = 'left')
    se_ss = se_ss.merge(relative_role_mapping, on = ['role'], how = 'left')
    se_ss = se_ss.merge(relative_country_mapping, on = ['country'], how = 'left')
    se_ss = se_ss.merge(relative_emptype_mapping, on = ['employment_type'], how = 'left')

    se_ss['actual_per_diff'] = (se_ss['M'] - global_median) / global_median

    # Micro adjustment
    se_ss['mod_perc_level_micro'] = (se_ss['level_per_diff'] - se_ss['actual_per_diff'])
    se_ss['mod_perc_role_micro'] = (se_ss['role_per_diff'] - se_ss['actual_per_diff'])
    se_ss['mod_perc_country_micro'] = (se_ss['country_per_diff'] - se_ss['actual_per_diff'])
    se_ss['mod_perc_type_micro'] = (se_ss['type_per_diff'] - se_ss['actual_per_diff'])

    # Macro adjustment
    ## Level
    level_mod_est = relative_level_yoe_mapping.merge(
                    se_ss.groupby(['yoe', 'level'])['M'].agg('median').reset_index(), 
                    on = ['yoe', 'level'], how = 'left')
    
    level_mod_est['actual_per_diff'] = (level_mod_est['M'] - global_median) / global_median
    level_mod_est['mod_perc_level_macro'] = (level_mod_est['level_per_diff'] - level_mod_est['actual_per_diff'])
    level_mod_est = level_mod_est[['yoe', 'level', 'mod_perc_level_macro']]
    se_ss = se_ss.merge(level_mod_est, on = ['yoe', 'level'], how = 'left')
    
    ## Emp Type
    type_mod_est = relative_emptype_mapping.merge(
                    se_ss.groupby(['employment_type'])['M'].agg('median').reset_index(), 
                    on = ['employment_type'], how = 'left')
    type_mod_est['actual_per_diff'] = (type_mod_est['M'] - global_median) / global_median
    type_mod_est['mod_perc_type_macro'] = (type_mod_est['type_per_diff'] - type_mod_est['actual_per_diff'])
    type_mod_est = type_mod_est[['employment_type', 'mod_perc_type_macro']]
    se_ss = se_ss.merge(type_mod_est, on = ['employment_type'], how = 'left')
    
    ## Role
    role_mod_est = relative_role_mapping.merge(
                    se_ss.groupby(['role'])['M'].agg('median').reset_index(), 
                    on = ['role'], how = 'left')
    role_mod_est['actual_per_diff'] = (role_mod_est['M'] - global_median) / global_median
    role_mod_est['mod_perc_role_macro'] = (role_mod_est['role_per_diff'] - role_mod_est['actual_per_diff'])
    role_mod_est = role_mod_est[['role', 'mod_perc_role_macro']]
    se_ss = se_ss.merge(role_mod_est, on = ['role'], how = 'left')
    
    # Country
    country_mod_est = relative_country_mapping.merge(
                    se_ss.groupby(['country'])['M'].agg('median').reset_index(), 
                    on = ['country'], how = 'left')
    country_mod_est['actual_per_diff'] = (country_mod_est['M'] - global_median) / global_median
    country_mod_est['mod_perc_country_macro'] = (country_mod_est['country_per_diff'] - country_mod_est['actual_per_diff'])
    country_mod_est = country_mod_est[['country', 'mod_perc_country_macro']]
    se_ss = se_ss.merge(country_mod_est, on = ['country'], how = 'left')
    
    
    
    se_ss['per_adjust'] = (se_ss['mod_perc_level_macro'] + se_ss['mod_perc_level_micro'])/2
    
    se_ss['M_adjusted'] = (1 + se_ss['per_adjust']) * se_ss['M']
    se_ss['M_adjusted'] = (1 + se_ss['mod_perc_type_macro']) * se_ss['M_adjusted']
    se_ss['M_adjusted'] = (1 + se_ss['mod_perc_role_macro']) * se_ss['M_adjusted']
    se_ss['M_adjusted'] = (1 + se_ss['mod_perc_country_macro']) * se_ss['M_adjusted']

    return(se_ss)

# error_df = se_ss[~(se_ss['median_salary'].isna())
#                          & (se_ss['employment_type'] != 'contract')]

# error_df.loc[:, 'diff_pre'] = (error_df['M'] - error_df['median_salary'])
# error_df.loc[:, 'diff_post'] = (error_df['M_adjusted'] - error_df['median_salary'])

# error_df.loc[:, 'abs_diff_pre'] = abs(error_df.loc[:, 'diff_pre'])
# error_df.loc[:, 'abs_diff_post'] = abs(error_df.loc[:, 'diff_post'])

# print(np.mean(error_df['abs_diff_pre']), np.mean(error_df['abs_diff_post']))

# error_df.to_csv('z.csv')

# error_df.groupby('level')['diff_post'].agg('mean')

