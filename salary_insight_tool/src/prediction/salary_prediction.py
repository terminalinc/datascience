def salary_df_gen():
    import pandas as pd
    import numpy as np
    
    job_final_df = pd.read_csv("data/intermediate/job_df_final.csv")
    job_final_df = job_final_df[['id', 'date', 'salary', 'country', 'experience_level',
                                   'min_years_of_experience', 'employment_type',
                                   'source_table', 'role']]
    job_final_df.columns = ['id', 'date', 'salary', 'country', 'job_level'
                            ,'yoe', 'employment_type', 
                            'source_table', 'role']
    
    cds_df_final = pd.read_csv("data/intermediate/cds_df_final.csv")
    cds_df_final.columns = ['id', 'date', 'country', 'yoe', 'skill_list', 'role',
                                'salary', 'employment_type', 'source_table']
    
    mem_final_df = pd.read_csv("data/intermediate/mem_df_final.csv")
    mem_final_df.columns = ['id', 'date', 'hourly_rate', 'salary', 'country', 
                            'level','skill_list', 'employment_type', 
                            'source_table', 'role']
    
    salary_df_nonencoded = pd.concat([job_final_df, cds_df_final, mem_final_df], axis = 0)
    
    # Type encoding
    mem_final_df['type_encode'] = np.where(mem_final_df['employment_type'] == 'full_time', 0, 1)
    job_final_df['type_encode'] = np.where(job_final_df['employment_type'] == 'full_time', 0, 1)
    cds_df_final['type_encode'] = np.where(cds_df_final['employment_type'] == 'full_time', 0, 1)
    
    # Level Encoding
    mem_final_df['level'] = mem_final_df['level'].fillna('L0')
    mem_final_df['level_encode'] = [int(l.replace('L', '')) for l in mem_final_df['level']]
    
    job_final_df['level'] = job_final_df['job_level'].fillna('IC0')
    job_final_df['job_level_encode'] = [int(l.replace('M', 'IC').replace('IC', '')) for l in job_final_df['job_level']]
    
    # Years of experience Encoding
    cds_df_final['yoe'] = cds_df_final['yoe'].fillna('')
    job_final_df['yoe'] = job_final_df['yoe'].fillna('')
    
    def yeo_encoder(row):
    
        yoe_dict = {'ZERO_TWO': 1, 'TWO_FIVE': 2, 'FIVE_TEN': 3, 'TEN_PLUS': 4}
        
        if row['yoe'] in yoe_dict:
            return yoe_dict[row['yoe']]
        else: 
            return 0
            
    cds_df_final['yoe_encode'] = cds_df_final.apply(yeo_encoder, axis = 1)
    job_final_df['yoe_encode'] = job_final_df.apply(yeo_encoder, axis = 1)
    
    # Role Encoding
    def region_encoder(row):
        
        na_list = ['Canada', 'United States']
        
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
        
        if row['country'] in na_list:
            return 0
        elif row['country'] in latam_list:
            return 1
        elif row['country'] in eur_list:
            return 2
        else:
            return 3
    
    mem_final_df['region_encode'] = mem_final_df.apply(region_encoder, axis= 1)
    cds_df_final['region_encode'] = cds_df_final.apply(region_encoder, axis= 1)
    job_final_df['region_encode'] = job_final_df.apply(region_encoder, axis= 1)
    
    # Role Encoding
    mem_final_df['role'] = mem_final_df['role'].fillna('')
    cds_df_final['role'] = cds_df_final['role'].fillna('')
    job_final_df['role'] = job_final_df['role'].fillna('')
    
    def role_encoder(row):
        role_dict = {'Backend': 0, 
                    'Full Stack': 1, 
                    'Frontend': 2, 
                    'Eng. Lead': 3, 
                    'Mobile': 4, 
                    'DevOps': 5, 
     
                    'Manual QA': 6,
                    'Automation QA': 7,
                    
                    'Data Analyst': 8, 
                    'Data Science': 9, 
                    'Data Engineer': 10,
                    'AI/ML': 11,
                    
                    'Designer': 12,
                    'Product Management': 13, 
                    'Scrum Master': 14, 
                    '': 15}
        
        return role_dict[row['role']]
    
    mem_final_df['role_encode'] = mem_final_df.apply(role_encoder, axis= 1)
    cds_df_final['role_encode'] = cds_df_final.apply(role_encoder, axis= 1)
    job_final_df['role_encode'] = job_final_df.apply(role_encoder, axis= 1)
    
    # Northamerican country encoding
    mem_final_df['na_country_encode'] = np.where(mem_final_df['region_encode'] == 0, 1, 0)
    cds_df_final['na_country_encode'] = np.where(cds_df_final['region_encode'] == 0, 1, 0)
    job_final_df['na_country_encode'] = np.where(job_final_df['region_encode'] == 0, 1, 0)
    
    def latam_encoder(row):
        latam_dict = ({ 'Costa Rica': 1, 'El Salvador': 2, 'Guatemala': 3, 
                    'Honduras': 4, 'Mexico': 5, 'Nicaragua': 6, 'Panama': 7, 
                    'Argentina': 8, 'Bolivia': 9, 'Brazil': 10, 'Chile': 11, 'Colombia': 12, 
                    'Ecuador': 13, 'Guyana': 14, 'Paraguay': 15, 'Peru': 16, 'Suriname': 17, 
                    'Uruguay': 18, 'Venezuela': 19, 'Cuba': 20, 'Dominican Republic': 21, 
                    'Haiti': 22, 'Belize': 23})
        
        if row['country'] in latam_dict:
            return(latam_dict[row['country']])
        else:
            return 0
    mem_final_df['latam_country_encode'] = mem_final_df.apply(latam_encoder, axis = 1)
    cds_df_final['latam_country_encode'] = cds_df_final.apply(latam_encoder, axis = 1)
    job_final_df['latam_country_encode'] = job_final_df.apply(latam_encoder, axis = 1)
    
    def eur_encoder(row):
    
        eur_list = ({'Albania': 1, 'Andorra': 2, 'Armenia': 3, 'Austria': 4, 'Azerbaijan': 5, 
                     'Belarus': 6, 
                    'Belgium': 7, 'Bulgaria': 8, 'Croatia': 9, 'Cyprus': 10, 'Czechia': 11, 
                    'Denmark': 12, 
                    'Estonia': 13, 'Finland': 14, 'France': 15, 'Georgia': 16, 'Germany': 17, 
                    'Greece': 18, 
                    'Hungary': 19, 'Iceland': 20, 'Ireland': 21, 'Italy': 22, 'Kazakhstan': 23 , 
                    'Kosovo': 24, 
                    'Latvia': 25, 'Liechtenstein': 26, 'Lithuania': 27, 'Luxembourg': 28, 
                    'Malta': 29, 
                    'Moldova': 30, 'Monaco': 31, 'Montenegro': 32, 'Netherlands': 33, 
                    'North Macedonia': 34, 
                     'Poland': 35, 'Portugal': 36, 'Romania': 37, 'Russia': 38, 
                    'San Marino': 39, 
                    'Serbia': 40, 'Slovakia': 41, 'Slovenia': 42, 'Spain': 43, 'Sweden': 44, 
                    'Switzerland': 45, 
                    'Turkey': 46, 'Ukraine': 47, 'United Kingdom': 48, 'Norway': 49})
        
        if row['country'] in eur_list:
            return(eur_list[row['country']])
        else:
            return 0
    mem_final_df['eur_country_encode'] = mem_final_df.apply(eur_encoder, axis= 1)
    cds_df_final['eur_country_encode'] = cds_df_final.apply(eur_encoder, axis= 1)
    job_final_df['eur_country_encode'] = job_final_df.apply(eur_encoder, axis= 1)
    
    # Source table encode
    mem_final_df['source_table'] = 2
    cds_df_final['source_table'] = 0
    job_final_df['source_table'] = 1
    
    # Concat table data    
    salary_df = pd.concat(
                    [mem_final_df[['salary', 'type_encode',
                           'level_encode', 'region_encode', 'role_encode', 'na_country_encode',
                           'latam_country_encode', 'eur_country_encode', 'source_table']], 
                    cds_df_final[['salary','type_encode', 'yoe_encode',
                           'region_encode', 'role_encode', 'na_country_encode',
                           'latam_country_encode', 'eur_country_encode', 'source_table']], 
                    job_final_df[['salary', 'type_encode',
                           'job_level_encode', 'yoe_encode', 'region_encode', 'role_encode',
                           'na_country_encode', 'latam_country_encode', 'eur_country_encode', 
                           'source_table']]
                    ], axis = 0)
    
    
    salary_df['yoe_encode'] = salary_df['yoe_encode'].fillna(0)
    salary_df['level_encode'] = salary_df['level_encode'].fillna(0)
    salary_df['job_level_encode'] = salary_df['job_level_encode'].fillna(0)
    
    return salary_df, salary_df_nonencoded


def global_outlier_range(salary_df):
    import pandas as pd
    import numpy as np
    
    outlier_df = pd.DataFrame()

    for r in list(salary_df.columns)[1:]:
        for v in list(salary_df[r].unique()):
    
            s = salary_df[salary_df[r] == v]['salary']
            
            q3, q1 = np.percentile(s, [75 ,25],method ='midpoint')
            iqr = q3 - q1
            
            lower_outlier = q1 - (iqr*1.5)
            upper_outlier = q3 + (iqr*1.5)
            
            d = {'row': r, 'value': v, 'lower':lower_outlier, 'upper':upper_outlier}
            
            outlier_df = outlier_df._append(d, ignore_index=True)
    
    
    lower_bound = np.median(outlier_df[outlier_df['lower']>0]['lower'])
    upper_bound = np.median(outlier_df['upper'])
    
    output = pd.DataFrame({'global_lower_bound': [lower_bound], 'global_upper_bound': [upper_bound] })
    output.to_csv('data/reference/global_outlier_range.csv', index = False)

    print(lower_bound, upper_bound)    


def construct_salary_model(salary_df):
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestRegressor 
    from sklearn.model_selection import RandomizedSearchCV, train_test_split
    import joblib
    
    gor = pd.read_csv('data/reference/global_outlier_range.csv')
    salary_df_ss = salary_df[(salary_df['salary'] < gor['global_upper_bound'][0]) 
                          & (salary_df['salary']> gor['global_lower_bound'][0])]
    
    # Construct Train/Test set
    X_train, X_test, y_train, y_test = train_test_split(
        salary_df_ss[['type_encode', 'level_encode', 'region_encode', 'role_encode',
               'na_country_encode', 'latam_country_encode', 'eur_country_encode',
               'source_table', 'yoe_encode', 'job_level_encode']], 
        salary_df_ss['salary'], test_size=0.1)
    
    
    model = RandomForestRegressor(n_estimators = 1400,
                                    min_samples_split = 12,
                                    min_samples_leaf =  1,
                                    max_features =  'sqrt',
                                    max_depth = 10,
                                    bootstrap =  True)
    model.fit(X_train, y_train)
    #print(np.mean(abs(model.predict(X_test) - y_test)))
    
    # save model
    joblib.dump(model, 'src/model/salary_prediction.sav')


# salary_df = salary_df_gen()[0]
# global_outlier_range(salary_df)
# construct_salary_model(salary_df)
