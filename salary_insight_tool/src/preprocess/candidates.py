def id_new_candidate_ids():
    
    import pandas as pd
    from src.model.role_prediction import predict_role
    
    cds_df = pd.read_csv("data/input/candidate/candidate_salary.csv")
    cds_role_df = pd.read_csv("data/input/candidate/desired_role.csv")
    candidate_role_mapping = pd.read_csv("data/reference/candidate_role_mapping.csv") 
    
    all_cds_ids = list(set(list(cds_df['candidate_id']) + list(cds_role_df['candidate_id'])))
    current_ids = list(set(candidate_role_mapping['candidate_id']))
    
    new_ids = list(set(current_ids) - set(all_cds_ids))
    crm_new = pd.DataFrame({'candidate_id':new_ids})

    crm_new = (pd.merge(crm_new, cds_df[['candidate_id', 'skill_list']], 
                                      on = 'candidate_id', how = 'left'))

    # Identify candidates that have applied to less than 4 roles
    unique_role_id_list = cds_role_df.groupby('candidate_id')['desired_role'].agg('count').reset_index()
    unique_role_id_list = list(unique_role_id_list[unique_role_id_list['desired_role'] < 4]['candidate_id'])
    
    crm_new = (pd.merge(crm_new, 
                        cds_role_df[cds_role_df['candidate_id'].isin(unique_role_id_list)]
                        [['candidate_id', 'desired_role']], 
                            on = 'candidate_id', how = 'left'))
    
    if len(crm_new)>0:
    
        no_role = crm_new[~(crm_new['skill_list'].isna()) 
                        & (crm_new['desired_role'].isna())
                        & (crm_new['predicted_role'].isna())]
        
        no_role = no_role[['candidate_id', 'skill_list']]
        
        results = predict_role(no_role, ['candidate_id'], 'skill_list')
        results['desired_role'] = ''
        
        crm_new = crm_new.merge(results, on = ['candidate_id', 'skill_list'],
                      how = 'left')
    
        candidate_role_mapping = (pd.concat([candidate_role_mapping,crm_new], axis = 0))
        
        candidate_role_mapping.to_csv("data/reference/candidate_role_mapping.csv", index = False)
    
    print('New Candidate IDs stored')

    
def process_cds_fulltime(cds_df):
    import pandas as pd
    usd_conv_df = pd.read_csv("data/reference/usd_conversion_table.csv") 
    currency_ref_df = pd.read_csv("data/reference/currency_ref_df.csv")
    currency_ref_df['date'] = pd.to_datetime(currency_ref_df['date'])
    currency_ref_df['date'] = [d.date() for d in currency_ref_df['date']]
    
    ft_df = (cds_df[cds_df['employment_type'].isin(['FULL_TIME', 'FULL_TIME_AND_CONTRACT'])]
            [['candidate_id', 'created_at', 'country_clean', 'desired_salary_amount', 
              'desired_salary_currency', 'years_of_exp_range','skill_list', 'role']])
    
    # Convert all currency to USD & annual rates
    ft_df['date'] = pd.to_datetime(ft_df['created_at'])
    ft_df['date'] = [d.date() for d in ft_df['date']]
    ft_df['currency'] = ft_df['desired_salary_currency']
    
    ft_df = ft_df.merge(currency_ref_df, on = ['date', 'currency'], how = 'left')
    ft_df['rate'] = ft_df['rate'].fillna(1)  
    ft_df['desired_salary_amount'] = ft_df['desired_salary_amount'].fillna(0)
    
    ft_df['salary'] = ft_df['rate'] * ft_df['desired_salary_amount']
    
    ft_df = ft_df[['candidate_id', 'created_at', 'country_clean',
                   'years_of_exp_range', 'skill_list', 'role',
                   'salary']]
    ft_df.columns = ['id', 'date', 'country',
                   'experience_level', 'skill_list', 'role',
                   'salary']
    ft_df['employment_type'] = 'full_time'
    
    ft_df = ft_df[(ft_df['salary']>0) & ~(ft_df['role'].isna())]
    
    return ft_df

def process_cds_contract(cds_df):
    import pandas as pd
    
    cont_df = (cds_df[cds_df['employment_type'].isin(['CONTRACT', 'FULL_TIME_AND_CONTRACT'])]
            [['candidate_id', 'created_at', 'country_clean', 'contractor_rate', 
              'years_of_exp_range','skill_list', 'role']])
    
    cont_df['salary'] = cont_df['contractor_rate'] * 12
    
    cont_df = cont_df[['candidate_id', 'created_at', 'country_clean',
                   'years_of_exp_range', 'skill_list', 'role',
                   'salary']]
    cont_df.columns = ['id', 'date', 'country',
                   'experience_level', 'skill_list', 'role',
                   'salary']
    cont_df['employment_type'] = 'contract'
    
    cont_df = cont_df[(cont_df['salary']>0) 
                  & ~(cont_df['role'].isna())
                  & ~(cont_df['country'].isna())]
    
    return cont_df

def process_candidate_data():
    import pandas as pd
    import numpy as np
    
    cds_df = pd.read_csv("data/input/candidate/candidate_salary.csv")
    cds_role_df = pd.read_csv("data/input/candidate/desired_role.csv")
    ctry_conv_df = pd.read_csv("data/reference/country_conversion_table.csv")
    candidate_role_mapping = pd.read_csv("data/reference/candidate_role_mapping.csv") 
    
    curr_list = cds_df[~(cds_df['desired_salary_currency'].isna())]['desired_salary_currency'].unique()
    pd.DataFrame({'currency': curr_list}).to_csv("data/reference/currency_list.csv", index = False)
    
    # Clean Country Label
    cds_df.country = [str(v).strip() for v in cds_df.country]
    cds_df = cds_df.merge(ctry_conv_df, on='country', how= 'left')
    
    target_countries = (['Canada', 'Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 
                'Honduras', 'Mexico', 'Nicaragua', 'Panama', 
                'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 
                'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 
                'Uruguay', 'Venezuela', 'Cuba', 'Dominican Republic', 'Haiti', 
                'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 
                'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 
                'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 
                'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 
                'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 
                'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 
                'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 
                'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 
                'Turkey', 'Ukraine', 'United Kingdom'])
    
    cds_df = cds_df[cds_df['country_clean'].isin(target_countries)]
    
    candidate_role_mapping['role'] = np.where(candidate_role_mapping['desired_role'].isna(), 
                                                candidate_role_mapping['predicted_role'], 
                                                candidate_role_mapping['desired_role'])
    cds_df = pd.merge(cds_df, candidate_role_mapping[['candidate_id', 'role']], 
                                  on = 'candidate_id', how = 'left')
        
    ft_df = process_cds_fulltime(cds_df)
    cont_df = process_cds_contract(cds_df)
    
    cds_df_final = pd.concat([ft_df, cont_df], axis = 0)
    cds_df_final['source_table'] = 'candidate'
    
    cds_df_final.to_csv("data/intermediate/cds_df_final.csv", index = False)

    print('Candidate Data Cleaned & Stored: data/intermediate/cds_df_final.csv')

#id_new_candidate_ids()
#process_candidate_data()














