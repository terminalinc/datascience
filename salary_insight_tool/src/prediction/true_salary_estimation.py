def compile_salary_results():
    
    import pandas as pd
    import numpy as np
    import joblib
    from scipy.stats import bootstrap
    import random
    
    cds_df_final = pd.read_csv("data/intermediate/cds_df_final.csv")
    mem_final_df = pd.read_csv("data/intermediate/mem_df_final.csv")
    job_final_df = pd.read_csv("data/intermediate/job_df_final.csv")
    combo_ref_df = pd.read_csv("data/intermediate/combo_ref_df.csv")
    experience_level = pd.read_csv("data/reference/experience_level.csv")
    tpd_df = pd.read_csv("data/reference/3rd_party_data.csv") 
    loaded_rf = joblib.load('src/model/salary_prediction.sav')
    gor = pd.read_csv("data/reference/global_outlier_range.csv")
    
    test_combos = pd.read_csv("data/reference/test_combos.csv") 
    
    # Column formating
    cds_df_final.columns = ['id', 'date', 'country', 'yoe', 'skill_list', 'role',
                            'salary', 'employment_type', 'source_table']
    
    mem_final_df.columns = ['id', 'date', 'hourly_rate', 'salary', 'country', 
                            'level','skill_list', 'employment_type', 
                            'source_table', 'role']
    
    job_final_df.columns = ['id', 'position_count', 'date', 'salary', 'country', 
                            'job_level', 'yoe', 'skill_list', 'employment_type', 'role',
                            'source_table']
    
    tpd_df.columns = ['role', 'country', 'n', 'yoe', 'median_salary',
                      'salary_low', 'salary_high']
    
    ## table based prediction
    X_columns = ['type_encode', 'level_encode', 'region_encode', 'role_encode',
               'na_country_encode', 'latam_country_encode', 'eur_country_encode',
               'source_table', 'yoe_encode', 'job_level_encode']
    
    combo_ref_df['source_table'] = 0
    combo_ref_df['cds_predictions'] = loaded_rf.predict(combo_ref_df[X_columns])
    combo_ref_df['source_table'] = 1
    combo_ref_df['job_predictions'] = loaded_rf.predict(combo_ref_df[X_columns])
    combo_ref_df['source_table'] = 2
    combo_ref_df['mem_predictions'] = loaded_rf.predict(combo_ref_df[X_columns])
    
    # Candidate salary record count
    cds_df_final = cds_df_final[(cds_df_final['salary'] > (gor.loc[0, 'global_lower_bound'])) 
                 & (cds_df_final['salary'] < (gor.loc[0, 'global_upper_bound']))]
    
    cds_combo_count = cds_df_final.groupby(['country', 'role', 'yoe', 'employment_type'])['salary'].agg('count').reset_index()
    cds_combo_count.columns = ['country', 'role', 'yoe', 'employment_type', 'cds_n']
    
    combo_ref_df = combo_ref_df.merge(cds_combo_count, on = ['country', 'role', 'yoe', 'employment_type'], how = 'left')
    
    combo_ref_cds_ss = combo_ref_df[combo_ref_df['cds_n'] > 0].reset_index(drop=True)
    combo_ref_cds_ss['salary_sample_cds'] = ''
    combo_ref_cds_ss['salary_sample_cds'] = combo_ref_cds_ss['salary_sample_cds'].astype('object')
    
    for c in range(0, len(combo_ref_cds_ss)):
        
        country = combo_ref_cds_ss['country'][c]
        role = combo_ref_cds_ss['role'][c]
        yoe = combo_ref_cds_ss['yoe'][c]
        employment_type = combo_ref_cds_ss['employment_type'][c]
        
        s = list(cds_df_final[(cds_df_final['country'] == country)
                         & (cds_df_final['role'] == role)
                         & (cds_df_final['yoe'] == yoe)
                         & (cds_df_final['employment_type'] == employment_type)]['salary'])
        s_len = len(s)
        
        if s_len > 5:
            bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                    , n_resamples = 1000, method='basic')
            
            salary_lower_s = bootstrap_s.confidence_interval[0]
            salary_upper_s = bootstrap_s.confidence_interval[1]
            salary_median_s = (salary_lower_s + salary_upper_s)/2
            
            combo_ref_cds_ss.loc[c, 'salary_lower_cds'] = salary_lower_s
            combo_ref_cds_ss.loc[c, 'salary_upper_cds'] = salary_upper_s
            combo_ref_cds_ss.loc[c, 'salary_median_cds'] = salary_median_s
            combo_ref_cds_ss.at[c, 'salary_sample_cds'] = s#(random.sample(sorted(bootstrap_s.bootstrap_distribution), s_len))
            
        else:
            combo_ref_cds_ss.loc[c, 'salary_median_cds'] = np.median(s)
    
    
    # Job salary record count
    job_final_df = job_final_df[(job_final_df['salary'] > (gor.loc[0, 'global_lower_bound'])) 
                 & (job_final_df['salary'] < (gor.loc[0, 'global_upper_bound']))]
                            
    job_combo_count = job_final_df.groupby(['country', 'job_level', 'role', 'yoe', 'employment_type'])['salary'].agg('count').reset_index()
    job_combo_count.columns = ['country', 'job_level', 'role', 'yoe', 'employment_type', 'job_n']
    
    combo_ref_df = combo_ref_df.merge(job_combo_count, on = ['country', 'job_level','role', 'yoe', 'employment_type'], how = 'left')
    
    combo_ref_job_ss = combo_ref_df[combo_ref_df['job_n'] > 5].reset_index(drop=True)
    combo_ref_job_ss['salary_sample_job'] = ''
    combo_ref_job_ss['salary_sample_job'] = combo_ref_job_ss['salary_sample_job'].astype('object')

    for c in range(0, len(combo_ref_job_ss)):
        
        country = combo_ref_job_ss['country'][c]
        role = combo_ref_job_ss['role'][c]
        yoe = combo_ref_job_ss['yoe'][c]
        job_level = combo_ref_job_ss['job_level'][c]
        employment_type = combo_ref_job_ss['employment_type'][c]
        
        s = list(job_final_df[(job_final_df['country'] == country)
                         & (job_final_df['role'] == role)
                         & (job_final_df['yoe'] == yoe)
                         & (job_final_df['job_level'] == job_level)
                         & (job_final_df['employment_type'] == employment_type)]['salary'])
        
        s_len = len(s)
        
        if s_len > 5: 
            bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                    , n_resamples = 1000, method='basic')
            
            salary_lower_s = bootstrap_s.confidence_interval[0]
            salary_upper_s = bootstrap_s.confidence_interval[1]
            salary_median_s = (salary_lower_s + salary_upper_s)/2
            
            combo_ref_job_ss.loc[c, 'salary_lower_job'] = salary_lower_s
            combo_ref_job_ss.loc[c, 'salary_upper_job'] = salary_upper_s
            combo_ref_job_ss.loc[c, 'salary_median_job'] = salary_median_s
            combo_ref_job_ss.at[c, 'salary_sample_job'] = s#(random.sample(sorted(bootstrap_s.bootstrap_distribution), s_len))
        else:
            combo_ref_cds_ss.loc[c, 'salary_median_cds'] = np.median(s)
        
    # member salary record count
    mem_final_df = mem_final_df[(mem_final_df['salary'] > (gor.loc[0, 'global_lower_bound'])) 
                 & (mem_final_df['salary'] < (gor.loc[0, 'global_upper_bound']))]
    
    mem_combo_count = mem_final_df.groupby(['country', 'role', 'level', 'employment_type'])['salary'].agg('count').reset_index()
    mem_combo_count.columns = ['country', 'role', 'level', 'employment_type', 'mem_n']
    
    combo_ref_df = combo_ref_df.merge(mem_combo_count, on = ['country', 'role', 'level', 'employment_type'], how = 'left')
    
    combo_ref_mem_ss = combo_ref_df[combo_ref_df['mem_n'] > 5].reset_index(drop=True)
    combo_ref_mem_ss['salary_sample_mem'] = ''
    combo_ref_mem_ss['salary_sample_mem'] = combo_ref_mem_ss['salary_sample_mem'].astype('object')
    
    for c in range(0, len(combo_ref_mem_ss)):
        
        country = combo_ref_mem_ss['country'][c]
        role = combo_ref_mem_ss['role'][c]
        level = combo_ref_mem_ss['level'][c]
        employment_type = combo_ref_mem_ss['employment_type'][c]
        
        s = list(mem_final_df[(mem_final_df['country'] == country)
                         & (mem_final_df['role'] == role)
                         & (mem_final_df['level'] == level)
                         & (mem_final_df['employment_type'] == employment_type)]['salary'])
        s_len = len(s)
        if s_len > 5: 
            bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                    , n_resamples = 1000, method='basic')
            
            salary_lower_s = bootstrap_s.confidence_interval[0]
            salary_upper_s = bootstrap_s.confidence_interval[1]
            salary_median_s = (salary_lower_s + salary_upper_s)/2
            
            combo_ref_mem_ss.loc[c, 'salary_lower_mem'] = salary_lower_s
            combo_ref_mem_ss.loc[c, 'salary_upper_mem'] = salary_upper_s
            combo_ref_mem_ss.loc[c, 'salary_median_mem'] = salary_median_s 
            combo_ref_mem_ss.at[c, 'salary_sample_mem'] = s#(random.sample(sorted(bootstrap_s.bootstrap_distribution), s_len))
        else:
            combo_ref_cds_ss.loc[c, 'salary_median_cds'] = np.median(s)
        
    # Combine results   
    combo_ref_df = (combo_ref_df.merge(
                       combo_ref_cds_ss[['country', 'role', 'yoe', 'employment_type',
                                         'level', 'job_level', 
                                        'salary_lower_cds', 'salary_upper_cds', 
                                        'salary_median_cds', 'salary_sample_cds']], #.drop_duplicates(), 
                       on = ['country', 'role', 'yoe', 'level', 'job_level', 'employment_type'], 
                       how = 'left'))
    
    combo_ref_df = combo_ref_df.merge(
                       combo_ref_job_ss[['country', 'role', 'yoe', 'job_level', 'employment_type', 
                                         'level', 'salary_lower_job', 'salary_upper_job', 
                                         'salary_median_job', 'salary_sample_job']], 
                       on = ['country', 'role', 'yoe', 'level', 'job_level', 'employment_type'], 
                       how = 'left')
    
    combo_ref_df = (combo_ref_df.merge(
                       combo_ref_mem_ss[['country', 'role', 'level', 'employment_type', 
                                         'yoe', 'job_level', 'salary_lower_mem', 'salary_upper_mem', 
                                         'salary_median_mem', 'salary_sample_mem']], 
                       on = ['country', 'role', 'yoe', 'level', 'job_level', 'employment_type'], 
                       how = 'left'))
    
    # Join 3rd Party Data
    combo_ref_df = combo_ref_df.merge(tpd_df[['role', 'country', 'yoe', 
                                              'median_salary', 'salary_low',
                                              'salary_high']].drop_duplicates(), 
                                      on = ['role', 'country', 'yoe'], how = 'left')
    
    combo_ref_df['cds_n'] = combo_ref_df['cds_n'].fillna(0)
    combo_ref_df['job_n'] = combo_ref_df['job_n'].fillna(0)
    combo_ref_df['mem_n'] = combo_ref_df['mem_n'].fillna(0)
    
    return combo_ref_df

#salary_estimates_raw = compile_salary_results()
#salary_estimates_raw.to_csv('d.csv')

def salary_est(row):
    import numpy as np
    
    lower_bound = 0
    upper_bound = 0
    salary_median = 0
    new_sample = []
    sample_size = 0
    confidence = 0
    
    n = 10
    
    if (row['cds_n'] >= n) & (row['job_n'] >= n) & (row['mem_n'] >= n):
            
        lower_bound = np.mean([row['salary_lower_cds'], row['salary_lower_job'], row['salary_lower_mem']])
        upper_bound = np.mean([row['salary_upper_cds'], row['salary_lower_job'], row['salary_upper_mem']])
        salary_median = np.mean([row['salary_median_cds'], row['salary_median_job'], row['salary_median_mem']])
        new_sample = (row['salary_sample_cds']
                         + row['salary_sample_job']
                         + row['salary_sample_mem'])
        sample_size = len(new_sample)
        confidence = 3

    elif (row['cds_n'] < n) & (row['job_n'] >= n) & (row['mem_n'] >= n):
    
        lower_bound = np.median([row['salary_lower_job'], row['salary_lower_mem']])
        upper_bound = np.median([row['salary_lower_job'], row['salary_upper_mem']])
        salary_median = np.median([row['cds_predictions'], row['salary_median_job'], row['salary_median_mem']])
        new_sample = (row['salary_sample_job']
                         + row['salary_sample_mem'])
        sample_size = len(new_sample)
        confidence = 2
        
    elif (row['cds_n'] < n) & (row['job_n'] < n) & (row['mem_n'] >= n):
    
        lower_bound = np.median([ row['salary_lower_mem']])
        upper_bound = np.median([ row['salary_upper_mem']])
        salary_median = np.median([row['cds_predictions'], row['job_predictions'], row['salary_median_mem']])
        new_sample = (row['salary_sample_mem'])
        sample_size = len(new_sample)
        confidence = 1
        
    elif (row['cds_n'] < n) & (row['job_n'] < n) & (row['mem_n'] < n):
            
        lower_bound = 0
        upper_bound = 0
        salary_median = np.median([row['cds_predictions'], row['job_predictions'], row['mem_predictions']])
        
    elif (row['cds_n'] >= n) & (row['job_n'] >= n) & (row['mem_n'] < n):
    
        lower_bound = np.median([row['salary_lower_cds'], row['salary_lower_job']])
        upper_bound = np.median([row['salary_upper_cds'], row['salary_lower_job']])
        salary_median = np.median([row['salary_median_cds'], row['salary_median_job'], row['mem_predictions']])
        new_sample = (row['salary_sample_cds']
                         + row['salary_sample_job'])
        sample_size = len(new_sample)
        confidence = 2
        
    elif (row['cds_n'] >= n) & (row['job_n'] < n) & (row['mem_n'] < n):
    
        lower_bound = np.median([row['salary_lower_cds']])
        upper_bound = np.median([row['salary_upper_cds']])
        salary_median = np.median([row['salary_median_cds'], row['job_predictions'], row['mem_predictions']])
        new_sample = (row['salary_sample_cds'])
        sample_size = len(new_sample)
        confidence = 1
        
    elif (row['cds_n'] >= n) & (row['job_n'] < n) & (row['mem_n'] >= n):
    
        lower_bound = np.median([row['salary_lower_cds'], row['salary_lower_mem']])
        upper_bound = np.median([row['salary_upper_cds'], row['salary_upper_mem']])
        salary_median = np.median([row['salary_median_cds'], row['job_predictions'], row['salary_median_mem']])
        new_sample = (row['salary_sample_cds']
                         + row['salary_sample_mem'])
        sample_size = len(new_sample)
        confidence = 2
        
    elif (row['cds_n'] < n) & (row['job_n'] >= n) & (row['mem_n'] < n):
    
        lower_bound = np.median([row['salary_lower_job']])
        upper_bound = np.median([ row['salary_lower_job']])
        salary_median = np.median([row['cds_predictions'], row['salary_median_job'], row['mem_predictions']])
        new_sample = (row['salary_sample_job'])
        sample_size = len(new_sample)
        confidence = 1

    return [salary_median, new_sample, sample_size, confidence]                  
   
#salary_estimates_raw[['L', 'M', 'U', 'figure_data']] = salary_estimates_raw.apply(salary_est, axis = 1, result_type='expand')
#salary_estimates_raw.to_csv('d.csv')

    







