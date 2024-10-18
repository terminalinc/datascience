# Generate baseline salary estimates
def baseline_model():
    import pandas as pd
    import datetime
    
    cds_ref = pd.read_csv('data/intermediate/flattened_cds_df.csv')
    role_skill_list = pd.read_csv('data/intermediate/role_skill_list.csv')

    cds_cand_level = (cds_ref[['candidate_id', 'desired_role', 
                             'country_clean', 'years_of_exp_range',
                             'annual_usd_salary']]).drop_duplicates()
    
    # Role Level
    s_role = (cds_cand_level.groupby(['desired_role'])['annual_usd_salary']
                .agg(['median', 'count']).reset_index())
    s_role['years_of_exp_range'] = 'all'
    s_role['country_clean'] = 'all'
    s_role['skill'] = 'all'
    
    # Role & Experience level
    s_role_yoe = (cds_cand_level.groupby(['desired_role', 'years_of_exp_range'])
                                ['annual_usd_salary']
                                .agg(['median', 'count']).reset_index())
    s_role_yoe['country_clean'] = 'all'
    s_role_yoe['skill'] = 'all'
    
    # Role, Experience & Country level
    s_role_yoe_ctry = (cds_cand_level.groupby(['desired_role', 'years_of_exp_range', 'country_clean'])
                                    ['annual_usd_salary']
                                    .agg(['median', 'count']).reset_index())
    s_role_yoe_ctry['skill'] = 'all'
    
    # Join top skills data
    cds_ref = cds_ref.merge(role_skill_list, on = ['desired_role', 'skill'], how = 'left')
    cds_ref_skill_df = cds_ref[cds_ref['top_skill'] == 1]
    
    # Generate skill based salary estimates
    s_role_skill = (cds_ref_skill_df.groupby(['desired_role', 'skill'])
                                    ['annual_usd_salary']
                                    .agg(['median', 'count']).reset_index())
    s_role_skill['years_of_exp_range'] = 'all'
    s_role_skill['country_clean'] = 'all'
    
    s_role_skill_yoe = (cds_ref_skill_df.groupby(['desired_role', 'skill', 'years_of_exp_range'])
                                        ['annual_usd_salary']
                                        .agg(['median', 'count']).reset_index())
    s_role_skill_yoe['country_clean'] = 'all'
    
    s_role_skill_yoe_ctry = (cds_ref_skill_df
                                        .groupby(['desired_role', 'skill', 'country_clean', 'years_of_exp_range'])
                                        ['annual_usd_salary']
                                        .agg(['median', 'count']).reset_index())
    
    # Merge Results
    salary_est = pd.concat([s_role, s_role_yoe], axis=0) 
    salary_est = pd.concat([salary_est, s_role_yoe_ctry], axis=0) 
    salary_est = pd.concat([salary_est, s_role_skill], axis=0) 
    salary_est = pd.concat([salary_est, s_role_skill_yoe], axis=0) 
    salary_est = pd.concat([salary_est, s_role_skill_yoe_ctry], axis=0) 
        
    ## TODO round up salary to whole number
    
    # Pull current date and time
    d = str(datetime.datetime.now().strftime("%Y%b%d_%H%MH"))

    # Output salary estimates
    (salary_est[['desired_role', 'years_of_exp_range','country_clean', 'skill',
                'median', 'count',]]
        .to_csv(f'data/output/salary_est_{d}.csv', index = False))
    
    print(f'Salary estimates saved as data/output/salary_est_{d}.csv  \n')
    
