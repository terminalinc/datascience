def process_jobs_data():
    
    import pandas as pd
    import joblib
    import numpy as np
    from src.model.role_prediction import predict_role
    
    job_ft = pd.read_csv("data/input/job/job_ft.csv")
    job_cont = pd.read_csv("data/input/job/job_contractor.csv")
        
    job_ft['source_table'] = 'jobs'
    job_cont['source_table'] = 'jobs'
    job_ft['employment_type'] = 'full_time'
    job_cont['employment_type'] = 'contract'
    
    # Join member contract and fulltime data into mem_df
    job_df = pd.concat([job_ft, job_cont], axis=0).reset_index(drop=True)
        
    # Remove all RMP-only enteries
    job_df = job_df[~job_df['max_salary'].isin([9999999, 999999])]
    
    # Remove all enteries where the role name and skills is missing
    job_df = job_df[~((job_df['role_name'].isna()) & (job_df['required_skills'].isna()))]
    
    # Combine required and nice to have skills together
    job_df['skills'] = job_df.loc[:, 'required_skills'].astype(str) + ',' + job_df.loc[:, 'nice_to_have_skills'].astype(str)
    
    # Predict roles for enteries without a role but have skills
    jobs_role_skills = job_df[(job_df['role_name'].isna())][['job_id', 'created_at', 'role_name', 'skills']]
    
    index = ['job_id', 'created_at', 'role_name']
    skills_list = 'skills'

    results = predict_role(jobs_role_skills, index, skills_list)
    
    results['job_id'] = results['job_id'].astype(str)
    job_df['job_id'] = job_df['job_id'].astype(str)
    
    job_df_pred = pd.merge(job_df, results, 
                                on = ['job_id', 'created_at', 'role_name', 'skills'], 
                                how = 'left')
        
    job_df_pred['role'] = np.where((job_df_pred['role_name'] != '') & (job_df_pred['predicted_role'].isna()), 
                                   job_df_pred['role_name'], 
                                   job_df_pred['predicted_role'])
    
    # Flatten location
    job_location_df = pd.DataFrame()
    
    for i in range(0, len(job_df_pred)):
        if pd.isna(job_df_pred['location_list'][i]) != True:
        
            ss_df = pd.DataFrame({'job_id': job_df_pred['job_id'][i], 
                                  'created_at': job_df_pred['created_at'][i], 
                                  'role': job_df_pred['role'][i], 
                                  'level': job_df_pred['level'][i], 
                                  'min_years_of_experience': job_df_pred['min_years_of_experience'][i],
                                  'skills': job_df_pred['skills'][i],
                                  'job_position_count': job_df_pred['job_position_count'][i],
                                  'employment_type': job_df_pred['employment_type'][i],
                                  
                                  'location': job_df_pred['location_list'][i].split(';'), 
                                  
                                  'min_salary' : job_df_pred['min_salary'][i],
                                  'max_salary' : job_df_pred['max_salary'][i],
                                  'min_contract_rate' : job_df_pred['min_contract_rate'][i],
                                  'max_contract_rate' : job_df_pred['max_contract_rate'][i],
                                  'latam_min_salary' : job_df_pred['latam_min_salary'][i],
                                  'latam_max_salary' : job_df_pred['latam_max_salary'][i],
                                  'canada_min_salary' : job_df_pred['canada_min_salary'][i],
                                  'canada_max_salary' : job_df_pred['canada_max_salary'][i],
                                  'europe_min_salary' : job_df_pred['europe_min_salary'][i],
                                  
                                  'europe_max_salary' : job_df_pred['europe_max_salary'][i],
                                  'latam_min_contractor_rate' : job_df_pred['latam_min_contractor_rate'][i],
                                  'latam_max_contractor_rate' : job_df_pred['latam_max_contractor_rate'][i],
                                  'canada_min_contractor_rate' : job_df_pred['canada_min_contractor_rate'][i],
                                  'canada_max_contractor_rate' : job_df_pred['canada_max_contractor_rate'][i],
                                  'europe_min_contractor_rate' : job_df_pred['europe_min_contractor_rate'][i],
                                  'europe_max_contractor_rate' : job_df_pred['europe_max_contractor_rate'][i],
                                 })
        else:
            ss_df = pd.DataFrame({'job_id': job_df_pred['job_id'][i], 
                                  'created_at': job_df_pred['created_at'][i], 
                                  'role': job_df_pred['role'][i], 
                                  'level': job_df_pred['level'][i], 
                                  'min_years_of_experience': job_df_pred['min_years_of_experience'][i],
                                  'skills': job_df_pred['skills'][i],
                                  'job_position_count': job_df_pred['job_position_count'][i],
                                  'employment_type': job_df_pred['employment_type'][i],
                                  
                                  'location': ['all'],
                                  
                                  'min_salary' : job_df_pred['min_salary'][i],
                                  'max_salary' : job_df_pred['max_salary'][i],
                                  'latam_min_salary' : job_df_pred['latam_min_salary'][i],
                                  'latam_max_salary' : job_df_pred['latam_max_salary'][i],
                                  'canada_min_salary' : job_df_pred['canada_min_salary'][i],
                                  'canada_max_salary' : job_df_pred['canada_max_salary'][i],
                                  'europe_min_salary' : job_df_pred['europe_min_salary'][i],
                                  'europe_max_salary' : job_df_pred['europe_max_salary'][i],
                                  
                                  'min_contract_rate' : job_df_pred['min_contract_rate'][i],
                                  'max_contract_rate' : job_df_pred['max_contract_rate'][i],
                                  'latam_min_contractor_rate' : job_df_pred['latam_min_contractor_rate'][i],
                                  'latam_max_contractor_rate' : job_df_pred['latam_max_contractor_rate'][i],
                                  'canada_min_contractor_rate' : job_df_pred['canada_min_contractor_rate'][i],
                                  'canada_max_contractor_rate' : job_df_pred['canada_max_contractor_rate'][i],
                                  'europe_min_contractor_rate' : job_df_pred['europe_min_contractor_rate'][i],
                                  'europe_max_contractor_rate' : job_df_pred['europe_max_contractor_rate'][i],
                                     })
            
        job_location_df = pd.concat([job_location_df, ss_df], axis=0)
    
    
    # Clean up location column
    job_location_df['location'] = [str(l).strip() for l in job_location_df['location']]
    job_location_df.loc[job_location_df['location'] == 'Toronto', 'location'] = 'Canada'
    job_location_df.loc[job_location_df['location'] == 'Kitchener-Waterloo', 'location'] = 'Canada'
    job_location_df.loc[job_location_df['location'] == 'Montreal', 'location'] = 'Canada'
    job_location_df.loc[job_location_df['location'] == 'Guadalajara', 'location'] = 'Mexico'
    job_location_df = job_location_df.fillna(0)
    
    job_location_df.columns = (['id',
                                 'date',
                                 'role',
                                 'level',
                                 'min_years_of_experience',
                                 'skills',
                                 'job_position_count',
                                 'employment_type',
                                 'country',
                                 'us_min',
                                 'us_max',
                                 'us_min_rate',
                                 'us_max_rate',
                                 'latam_min',
                                 'latam_max',
                                 'can_min',
                                 'can_max',
                                 'eur_min',
                                 'eur_max',
                                 'latam_min_rate',
                                 'latam_max_rate',
                                 'can_min_rate',
                                 'can_max_rate',
                                 'eur_min_rate',
                                 'eur_max_rate'])
    
    # Remove rows where country is missing
    job_location_df = job_location_df[job_location_df['country'] != 'all']
    job_location_df['salary'] = 0
    
    def map_geo_salary(row):
        
        latam_list = (['Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 
                    'Honduras', 'Mexico', 'Nicaragua', 'Panama', 
                    'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 
                    'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 
                    'Uruguay', 'Venezuela', 'Cuba', 'Dominican Republic', 'Haiti'])
    
        eur_list = (['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 
                    'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 
                    'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 
                    'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 
                    'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 
                    'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 
                    'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 
                    'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 
                    'Turkey', 'Ukraine', 'United Kingdom'])
    
        salary = 0
        
        # if row.country == 'all':
    
        #     min_all = max(row.us_min, row.can_min, row.latam_min, row.eur_min)
        #     max_all = max(row.us_max, row.can_max, row.latam_max, row.eur_max)
            
        #     if (min_all != 0) & (max_all != 0) & (min_all != max_all):
        #         salary = (min_all + max_all) / 2
        #     elif (min_all != 0) & (max_all != 0) & (min_all == max_all):
        #         salary = max(min_all, max_all)
        #     elif (min_all != 0) | (max_all != 0):
        #         salary = max(min_all, max_all)
        #     else:
        #         salary = 0
    
        # if row.country == 'United States':
                
        #     min_all = max(row.us_min, row.can_min)
        #     max_all = max(row.us_max, row.can_max)
            
        #     if (min_all != 0) & (max_all != 0) & (min_all != max_all):
        #         salary = (min_all + max_all) / 2
        #     elif (min_all != 0) & (max_all != 0) & (min_all == max_all):
        #         salary = max(min_all, max_all)
        #     elif (min_all != 0) | (max_all != 0):
        #         salary = max(min_all, max_all)
        #     else:
        #         salary = 0
                
        if (row.country == 'Canada') & (row.employment_type == 'full_time'):
            
            min_all = max(row.us_min, row.can_min)
            max_all = max(row.us_max, row.can_max)
            
            if (min_all != 0) & (max_all != 0) & (min_all != max_all):
                salary = (min_all + max_all) / 2
            elif (min_all != 0) & (max_all != 0) & (min_all == max_all):
                salary = max(min_all, max_all)
            elif (min_all != 0) | (max_all != 0):
                salary = max(min_all, max_all)
            else:
                salary = 0
                
        elif (row.country in (latam_list)) & (row.employment_type == 'full_time'):
            
            if (row.latam_min != 0) & (row.latam_max != 0) & (row.latam_min != row.latam_max):
                salary = (row.latam_min + row.latam_max) / 2
            elif (row.latam_min != 0) & (row.latam_max != 0) & (row.latam_min == row.latam_max):
                salary = max(row.latam_min, row.latam_max)
            elif (row.latam_min != 0) | (row.latam_max != 0):
                salary = max(row.latam_min, row.latam_max)
            else:
                salary = 0
            
        elif (row.country in (eur_list)) & (row.employment_type == 'full_time'):
            
            if (row.eur_min != 0) & (row.eur_max != 0) & (row.eur_min != row.eur_max):
                salary = (row.eur_min + row.eur_max) / 2
            elif (row.eur_min != 0) & (row.eur_max != 0) & (row.eur_min == row.eur_max):
                salary = max(row.eur_min, row.eur_max)
            elif (row.eur_min != 0) | (row.eur_max != 0):
                salary = max(row.eur_min, row.eur_max)
            else:
                salary = 0
                
        elif (row.country == 'Canada') & (row.employment_type == 'contract'):
            
            min_all = max(row.us_min_rate, row.can_min_rate)
            max_all = max(row.us_max_rate, row.can_max_rate)
                
            if (min_all != 0) & (max_all != 0) & (min_all != max_all):
                salary = ((min_all + max_all) / 2) * 12
            elif (min_all != 0) & (max_all != 0) & (min_all == max_all):
                salary = max(min_all, max_all) * 12
            elif (min_all != 0) | (max_all != 0):
                salary = max(min_all, max_all) * 12
            else:
                salary = 0
                    
        elif (row.country in (latam_list)) & (row.employment_type == 'contract'):
                
            if (row.latam_min_rate != 0) & (row.latam_max_rate != 0) & (row.latam_min_rate != row.latam_max_rate):
                salary = ((row.latam_min_rate + row.latam_max_rate) / 2) * 12
            elif (row.latam_min_rate != 0) & (row.latam_max_rate != 0) & (row.latam_min_rate == row.latam_max_rate):
                salary = max(row.latam_min_rate, row.latam_max_rate) * 12
            elif (row.latam_min_rate != 0) | (row.latam_max_rate != 0):
                salary = max(row.latam_min_rate, row.latam_max_rate) * 12
                
            elif (row.latam_min_rate == 0) & (row.latam_max_rate == 0):
                
                min_all = max(row.us_min_rate, row.can_min_rate)
                max_all = max(row.us_max_rate, row.can_max_rate)
                    
                if (min_all != 0) & (max_all != 0) & (min_all != max_all):
                    salary = ((min_all + max_all) / 2) * 12
                elif (min_all != 0) & (max_all != 0) & (min_all == max_all):
                    salary = max(min_all, max_all) * 12
                elif (min_all != 0) | (max_all != 0):
                    salary = max(min_all, max_all) * 12
                else:
                    salary = 0
                
            else:
                salary = 0
                
        elif (row.country in (eur_list)) & (row.employment_type == 'contract'):
            
            if (row.eur_min_rate != 0) & (row.eur_max_rate != 0) & (row.eur_min_rate != row.eur_max_rate):
                salary = ((row.eur_min_rate + row.eur_max_rate) / 2) * 12
            elif (row.eur_min_rate != 0) & (row.eur_max_rate != 0) & (row.eur_min_rate == row.eur_max_rate):
                salary = max(row.eur_min_rate, row.eur_max_rate) * 12
            elif (row.eur_min_rate != 0) | (row.eur_max_rate != 0):
                salary = max(row.eur_min_rate, row.eur_max_rate) * 12
            
            elif (row.latam_min_rate == 0) & (row.latam_max_rate == 0):
                
                min_all = max(row.us_min_rate, row.can_min_rate)
                max_all = max(row.us_max_rate, row.can_max_rate)
                    
                if (min_all != 0) & (max_all != 0) & (min_all != max_all):
                    salary = ((min_all + max_all) / 2) * 12
                elif (min_all != 0) & (max_all != 0) & (min_all == max_all):
                    salary = max(min_all, max_all) * 12
                elif (min_all != 0) | (max_all != 0):
                    salary = max(min_all, max_all) * 12
                else:
                    salary = 0
                
            else:
                salary = 0
            
        return(salary)
    
    job_location_df['salary'] = job_location_df.apply(map_geo_salary, axis=1)
    job_location_df = (job_location_df[job_location_df['salary'] != 0].reset_index(drop=True)
                        [['id', 'date', 'role', 'level', 'min_years_of_experience', 'skills',
                        'job_position_count', 'employment_type', 'country','salary']])
    
    # Find outlier salaries
    q3, q1 = np.percentile(job_location_df['salary'], [75 ,25])
    iqr = q3 - q1
    
    lower_outlier = q1 - (iqr*2)
    upper_outlier = q3 + (iqr*2)
    
    job_location_df = (job_location_df[(job_location_df['salary']<upper_outlier)
                                    & (job_location_df['salary']>lower_outlier)]
                                    .reset_index(drop=True))
        
    job_final_df = pd.DataFrame()
    for i in range(0, len(job_location_df)):
        
            ss_df = pd.DataFrame({'id': job_location_df['id'][i], 
                                  'position_count': list(range(0,job_location_df['job_position_count'][i].astype(int))),
                                  #'job_position_count': job_location_df['job_position_count'][i],
                                  'date': job_location_df['date'][i],
                                  'salary': job_location_df['salary'][i],
                                  'country': job_location_df['country'][i],
                                  'experience_level': job_location_df['level'][i],
                                  'min_years_of_experience': job_location_df['min_years_of_experience'][i],
                                  'skill_list': job_location_df['skills'][i],
                                  'employment_type': job_location_df['employment_type'][i],                              
                                  'role': job_location_df['role'][i], 
                                 })
            job_final_df = pd.concat([job_final_df, ss_df], axis=0)
            
    job_final_df['source_table'] = 'job'
    job_final_df.to_csv("data/intermediate/job_df_final.csv", index = False)
    
    print('Jobs Data Cleaned & Stored: data/intermediate/job_df_final.csv')


# process_jobs_data()

