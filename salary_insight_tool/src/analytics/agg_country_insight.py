def agg_country(salary_estimates_raw):
    
    import pandas as pd
    from scipy.stats import bootstrap
    import numpy as np
    
    relative_country_mapping = pd.read_csv('data/reference/relative_country_mapping.csv')
    can_value = relative_country_mapping.loc[relative_country_mapping['country'] == 'Canada', 'country_per_diff'][0]
    relative_country_mapping.loc[relative_country_mapping['country'] == 'Canada', 'country_per_diff'] = can_value - 0.15
    relative_role_mapping = pd.read_csv('data/reference/relative_role_mapping.csv')
    
    df = salary_estimates_raw[['country', 'role', 'level', 'employment_type', 
                               'yoe', 'job_level','salary_sample_cds', 'salary_sample_job',
                               'salary_sample_mem', 'cds_predictions', 'job_predictions', 
                               'mem_predictions', 'cds_n', 'job_n', 'mem_n']]
    
    df['cds_len'] = [len((i)) for i in df['salary_sample_cds']]
    df['mem_len'] = [len((i)) for i in df['salary_sample_mem']]
    df['job_len'] = [len((i)) for i in df['salary_sample_job']]
    
    df['total_len'] = df['cds_len'] + df['mem_len'] + df['job_len'] 
        
    ref_list = df[df['total_len'] > 9].groupby(['country']).agg('count').reset_index()[['country']]
    ref_list = list(ref_list['country'])

    ref = pd.DataFrame()
    for i in ref_list:        
        df_ss = df[(df['country'] == i)]
        
        c_sample = df_ss[(df_ss['cds_len'] > 0) & (df_ss['salary_sample_cds'].notna())]
        j_sample = df_ss[(df_ss['job_len'] > 0) & (df_ss['salary_sample_job'].notna())]
        m_sample = df_ss[(df_ss['mem_len'] > 0) & (df_ss['salary_sample_mem'].notna())]

        cds_n = sum(c_sample['cds_n'])
        job_n = sum(j_sample['job_n'])
        mem_n = sum(m_sample['mem_n'])
                
        sample_list = []
        
        len(sample_list)
        
        [sample_list.extend(list(i)) for i in c_sample['salary_sample_cds']]
        [sample_list.extend(list(i)) for i in m_sample['salary_sample_mem']]
        [sample_list.extend(list(i)) for i in j_sample['salary_sample_job']]
        
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
                             'median': [np.median(full_list)], 
                             'figure_data': [sample_list], 
                             'cds_n': [cds_n], 
                             'job_n': [job_n], 
                             'mem_n': [mem_n], })
        ref = pd.concat([ref, data])
        
    se_ss = ref.copy()
    global_median = np.median(se_ss['median'])
    se_ss = se_ss.merge(relative_country_mapping, on = ['country'], how = 'left')
    se_ss['actual_per_diff'] = (se_ss['median'] - global_median) / global_median
    # se_ss['mod_perc_country_micro'] = (se_ss['country_per_diff'] - se_ss['actual_per_diff'])
    
    # Country
    country_mod_est = relative_country_mapping.merge(
                    se_ss.groupby(['country'])['median'].agg('median').reset_index(), 
                    on = ['country'], how = 'left')
    country_mod_est['actual_per_diff'] = (country_mod_est['median'] - global_median) / global_median
    country_mod_est['mod_perc_country_macro'] = (country_mod_est['country_per_diff'] - country_mod_est['actual_per_diff'])
    country_mod_est = country_mod_est[['country', 'mod_perc_country_macro']]
    se_ss = se_ss.merge(country_mod_est, on = ['country'], how = 'left')
    
    se_ss['M_adjusted'] = (1 + se_ss['mod_perc_country_macro']) * se_ss['median']
    
    se_ss['n'] = se_ss['cds_n'] + se_ss['job_n'] + se_ss['mem_n']
    se_ss['role'] = ''
    se_ss['level'] = ''
    se_ss['employment_type'] = ''
    se_ss['yoe'] = ''
    se_ss['job_level'] = ''
    se_ss['confidence'] = 'agg'
    
    se_ss_results = se_ss[['country', 'median','M_adjusted', 'figure_data', 
                           'cds_n', 'job_n', 'mem_n', 'role', 'level', 
                           'employment_type', 'yoe', 'job_level', 'n', 
                           'confidence']]
    
    return(se_ss_results)

