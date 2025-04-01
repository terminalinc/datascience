
salary_estimates_raw.columns

## Estimate salary insights

df = salary_estimates_raw[['country', 'role', 'level', 'employment_type', 'yoe', 'job_level',
              'salary_sample_cds', 'salary_sample_job','salary_sample_mem', 
              'cds_predictions', 'job_predictions', 'mem_predictions']]

df['cds_len'] = [len(str(i)) for i in df['salary_sample_cds']]
df['mem_len'] = [len(str(i)) for i in df['salary_sample_mem']]
df['job_len'] = [len(str(i)) for i in df['salary_sample_job']]

df['total_len'] = df['cds_len'] + df['mem_len'] + df['job_len'] 

ref_list = df[df['total_len'] > 9].groupby(['country', 'role']).agg('count').reset_index()[['country', 'role']]
ref_list = df[df['total_len'] > 9].groupby(['country', 'level']).agg('count').reset_index()[['country', 'level']]
ref_list = df[df['total_len'] > 9].groupby(['country']).agg('count').reset_index()[['country']]

ref_list = list(ref_list['country'])

###
# ref = pd.DataFrame()
# for i, k in zip(ref_list['country'], ref_list['role']):
#     print(i, k)
    
#     df_ss = df[(df['country'] == i) & (df['role'] == k)]
    
ref = pd.DataFrame()
for i, k in zip(ref_list['country'], ref_list['level']):
    print(i, k)
    
    df_ss = df[(df['country'] == i) & (df['level'] == k)]
    
# ref = pd.DataFrame()
# for i in ref_list:
#     print(i)
    
#     df_ss = df[(df['country'] == i)]


    # c = df_ss[(df_ss['cds_len'] > 0) & (df_ss['salary_sample_cds'].notna())]['salary_sample_cds']
    # m = df_ss[(df_ss['mem_len'] > 0) & (df_ss['salary_sample_mem'].notna())]['salary_sample_mem']
    # j = df_ss[(df_ss['job_len'] > 0) & (df_ss['salary_sample_job'].notna())]['salary_sample_job']    
    
    # full_list = []
    # c_list = []
    # m_list = []
    # j_list = []
    
    # [c_list.extend(list(i)) for i in c]
    # [m_list.extend(list(i)) for i in m]
    # [j_list.extend(list(i)) for i in j]
    
    # full_list.extend(c_list)
    # full_list.extend(m_list)
    # full_list.extend(j_list)
    
    # full_list.extend(j_list)
    # full_list.extend(j_list)
    # full_list.extend(j_list)
    
    bootstrap_c = bootstrap((df_ss['cds_predictions'],), np.median, confidence_level=0.95
                            , n_resamples = 1000, method='basic')
    bootstrap_j = bootstrap((df_ss['job_predictions'],), np.median, confidence_level=0.95
                            , n_resamples = 1000, method='basic')
    bootstrap_m = bootstrap((df_ss['mem_predictions'],), np.median, confidence_level=0.95
                            , n_resamples = 1000, method='basic')
    full_list = []
    full_list.extend(bootstrap_c.bootstrap_distribution)
    full_list.extend(bootstrap_j.bootstrap_distribution)
    full_list.extend(bootstrap_m.bootstrap_distribution)
    
    data = pd.DataFrame({'country': [i],
                         'level': [k],
                      'median': [np.median(full_list)], #np.median(bootstrap_s.bootstrap_distribution)],
                      'mean': [np.mean(full_list)], 
                      'len': [len(full_list)]})
    ref = pd.concat([ref, data])
    
ref.sort_values('median', ascending = False)
    
relative_level_yoe_mapping = pd.read_csv('data/reference/relative_level_yoe_mapping.csv')
relative_country_mapping = pd.read_csv('data/reference/relative_country_mapping.csv')
can_value = relative_country_mapping.loc[relative_country_mapping['country'] == 'Canada', 'country_per_diff'][0]
relative_country_mapping.loc[relative_country_mapping['country'] == 'Canada', 'country_per_diff'] = can_value - 0.05
relative_role_mapping = pd.read_csv('data/reference/relative_role_mapping.csv')

# 0.15 for country
# 0.1 for role
# 0.0 for level

se_ss = ref.copy()
global_median = np.median(se_ss['median'])

se_ss = se_ss.merge(relative_level_yoe_mapping, on = ['level'], how = 'left')
se_ss = se_ss.merge(relative_country_mapping, on = ['country'], how = 'left')
se_ss = se_ss.merge(relative_role_mapping, on = ['role'], how = 'left')

se_ss['actual_per_diff'] = (se_ss['median'] - global_median) / global_median

se_ss['mod_perc_country_micro'] = (se_ss['country_per_diff'] - se_ss['actual_per_diff'])

# Country
country_mod_est = relative_country_mapping.merge(
                se_ss.groupby(['country'])['median'].agg('median').reset_index(), 
                on = ['country'], how = 'left')
country_mod_est['actual_per_diff'] = (country_mod_est['median'] - global_median) / global_median
country_mod_est['mod_perc_country_macro'] = (country_mod_est['country_per_diff'] - country_mod_est['actual_per_diff'])
country_mod_est = country_mod_est[['country', 'mod_perc_country_macro']]
se_ss = se_ss.merge(country_mod_est, on = ['country'], how = 'left')

## Role
role_mod_est = relative_role_mapping.merge(
                se_ss.groupby(['role'])['median'].agg('median').reset_index(), 
                on = ['role'], how = 'left')
role_mod_est['actual_per_diff'] = (role_mod_est['median'] - global_median) / global_median
role_mod_est['mod_perc_role_macro'] = (role_mod_est['role_per_diff'] - role_mod_est['actual_per_diff'])
role_mod_est = role_mod_est[['role', 'mod_perc_role_macro']]
se_ss = se_ss.merge(role_mod_est, on = ['role'], how = 'left')
    
## Level
se_ss['mod_perc_level_micro'] = (se_ss['level_per_diff'] - se_ss['actual_per_diff'])

level_mod_est = relative_level_yoe_mapping.merge(
                se_ss.groupby(['level'])['median'].agg('median').reset_index(), 
                on = ['level'], how = 'left')

level_mod_est['actual_per_diff'] = (level_mod_est['median'] - global_median) / global_median
level_mod_est['mod_perc_level_macro'] = (level_mod_est['level_per_diff'] - level_mod_est['actual_per_diff'])
level_mod_est = level_mod_est[['yoe', 'level', 'mod_perc_level_macro']]
se_ss = se_ss.merge(level_mod_est, on = ['yoe', 'level'], how = 'left')
    
# Salary Adjustment
se_ss['per_adjust'] = (se_ss['mod_perc_level_macro'] + se_ss['mod_perc_level_micro'])/2

se_ss['median_adj'] = (1 + se_ss['per_adjust']) * se_ss['median']
se_ss['median_adj'] = (1 + se_ss['mod_perc_country_macro']) * se_ss['median_adj']# se_ss['median']
se_ss['median_adj'] = (1 + se_ss['mod_perc_role_macro']) * se_ss['median_adj']

se_ss['mean_adj'] = (1 + se_ss['per_adjust']) * se_ss['mean']
se_ss['mean_adj'] = (1 + se_ss['mod_perc_country_macro']) * se_ss['mean_adj']#se_ss['mean']
se_ss['mean_adj'] = (1 + se_ss['mod_perc_role_macro']) * se_ss['mean_adj']

se_ss_results = se_ss[['country', 'median', 'mean','median_adj', 'mean_adj']]
se_ss_results = se_ss[['country', 'role', 'median', 'mean','median_adj', 'mean_adj']]
se_ss_results = se_ss[['country', 'level', 'median', 'mean','median_adj', 'mean_adj']]

se_ss.columns

# se_ss_results.to_csv('temp_country_level.csv')

r = pd.read_csv("data/output/salary_estimates.csv")

r_agg = r.groupby(['country'])['M_adjusted'].agg('median').reset_index()
r_agg = r.groupby(['country', 'role'])['M_adjusted'].agg('median').reset_index()
r_agg = r.groupby(['country', 'level'])['M_adjusted'].agg('median').reset_index()

a = se_ss_results.merge(r_agg, on = ['country', 'role'])
a = se_ss_results.merge(r_agg, on = ['country', 'level'])

a.sort_values('country')    

a.to_csv('temp.csv')
    
    
    