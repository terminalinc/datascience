def region_label(row):
    
    na_list = ['Canada','United States']
    
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
    
    if row['country'] in latam_list:
        r = 'latin_america'
    elif row['country'] in eur_list:
        r = 'europe'
    elif row['country'] in na_list:
        r = 'north_america'
    else:
        r = ''
        
    return r

def create_salary_combo_df():    
    import pandas as pd
    import itertools
    import numpy as np
    
    mem_final_df = pd.read_csv("data/intermediate/mem_df_final.csv")
    job_final_df = pd.read_csv("data/intermediate/job_df_final.csv")
    cds_df_final = pd.read_csv("data/intermediate/cds_df_final.csv")
    experience_level = pd.read_csv("data/reference/experience_level.csv")

    def yeo_encoder(row):
    
        yoe_dict = {'ZERO_TWO': 1, 'TWO_FIVE': 2, 'FIVE_TEN': 3, 'TEN_PLUS': 4}
        
        if row['yoe'] in yoe_dict:
            return yoe_dict[row['yoe']]
        else: 
            return 0
        
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
    
    # Role Encoding
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
                    
    role_dict = {'Backend': 0, 'Full Stack': 1, 'Frontend': 2, 'Eng. Lead': 3, 
                'Mobile': 4, 'DevOps': 5, 'Manual QA': 6,'Automation QA': 7,
                'Data Analyst': 8, 'Data Science': 9, 'Data Engineer': 10,'AI/ML': 11,
                'Designer': 12, 'Product Management': 13, 'Scrum Master': 14}
        
    level_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']
    employment_type_list = ['full_time', 'contract']
    country_list = list(set(list(mem_final_df['country'].unique())
                        + list(job_final_df['country'].unique())
                        + list(cds_df_final['country'].unique())))
    
    combo_ref_df = pd.DataFrame(itertools.product(country_list,
                                                   role_dict.keys(), 
                                                   level_list, 
                                                   employment_type_list))
    combo_ref_df.columns = ['country', 'role', 'level', 'employment_type']
    combo_ref_df = pd.merge(combo_ref_df, experience_level, on= 'level', how = 'left')
    #combo_ref_df['region'] = combo_ref_df.apply(region_label, axis=1)
    
    # encoding
    combo_ref_df['type_encode'] = np.where(combo_ref_df['employment_type'] == 'full_time', 0, 1)
    combo_ref_df['level_encode'] = [int(l.replace('L', '')) for l in combo_ref_df['level']]
    combo_ref_df['job_level_encode'] = [int(l.replace('M', 'IC').replace('IC', '')) for l in combo_ref_df['job_level']]
    combo_ref_df['yoe_encode'] = combo_ref_df.apply(yeo_encoder, axis = 1)
    combo_ref_df['region_encode'] = combo_ref_df.apply(region_encoder, axis= 1)
    combo_ref_df['role_encode'] = combo_ref_df.apply(role_encoder, axis= 1)
    combo_ref_df['na_country_encode'] = np.where(combo_ref_df['region_encode'] == 0, 1, 0)
    combo_ref_df['latam_country_encode'] = combo_ref_df.apply(latam_encoder, axis = 1)
    combo_ref_df['eur_country_encode'] = combo_ref_df.apply(eur_encoder, axis= 1)
    combo_ref_df['source_table'] = 0
    
    combo_ref_df.to_csv("data/intermediate/combo_ref_df.csv", index = False)
    print('Combo Reference table constructed: data/intermediate/combo_ref_df.csv')
    
#create_salary_combo_df()