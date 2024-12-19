def combine_members_data():
    import pandas as pd
    
    # Import members related data
    mem_ft = pd.read_csv("data/input/member/member_ft.csv")
    mem_cont = pd.read_csv("data/input/member/member_contractor_dayforce.csv")
    mem_deel = pd.read_csv("data/reference/member_contractor_deel.csv")
    ctry_conv_df = pd.read_csv("data/reference/country_conversion_table.csv")
    usd_conv_df = pd.read_csv("data/reference/usd_conversion_table.csv") 
    currency_ref_df = pd.read_csv("data/reference/currency_ref_df.csv")
    currency_ref_df['date'] = pd.to_datetime(currency_ref_df['date'])

    # Join formatting data frames
    mem_ft = pd.merge(mem_ft, ctry_conv_df[['country_clean', 'member_country_code', 'currency']], left_on = 'country_code', right_on = 'member_country_code', how = 'left')
    #mem_ft = pd.merge(mem_ft, usd_conv_df[['country_clean', 'usd_per_unit']], on = 'country_clean', how = 'left')
    mem_cont = pd.merge(mem_cont, ctry_conv_df[['country_clean', 'member_country_code']], left_on = 'country_code', right_on = 'member_country_code', how = 'left')
    
    # Format Members fulltime data
    mem_ft_ss = mem_ft[(mem_ft['status'] != 'TERMINATED') & (mem_ft['currency'] != 'USD')]
    mem_ft_ss = mem_ft_ss[['employeeXRefCode', 'EffectiveStart', 'BaseRate', 
                            'BaseSalary', 'country_clean', 'level', 'department', 
                           'job_title', 'skill_list', 'currency']]
    
    mem_ft_ss['date'] = pd.to_datetime(mem_ft_ss['EffectiveStart'])
    mem_ft_ss = mem_ft_ss.merge(currency_ref_df, on = ['date', 'currency'], how = 'left')
    mem_ft_ss['emp_type'] = 'full_time'
    mem_ft_ss.loc[:,'BaseSalary'] = mem_ft_ss[['BaseSalary', 'rate']].product(axis=1)
    mem_ft_ss = mem_ft_ss.drop(['currency', 'rate', 'date'], axis=1)
    
    # Format members contract data
    # Note, mem_deel is already formatted
    mem_cont_ss = mem_cont[mem_cont['status'] != 'TERMINATED']
    mem_cont_ss = mem_cont_ss[['employeeXRefCode', 'EffectiveStart', 'BaseRate', 
                            'BaseSalary', 'country_clean', 'level', 'department', 
                           'job_title', 'skill_list']]
    mem_cont_ss['emp_type'] = 'contract'
    mem_cont_ss = pd.concat([mem_cont_ss, mem_deel], axis=0)
    
    # Join member contract and fulltime data into mem_df
    mem_df = pd.concat([mem_ft_ss, mem_cont_ss], axis=0).reset_index(drop=True)
    #mem_df.loc[mem_df.skill_list.isna(), 'skill_list'] = 'all'
    
    mem_df.columns = (['id', 'date', 
                       'hourly_rate', 'salary', 'country', 
                       'experience_level', 'department', 'job_title', 
                       'skill_list','employment_type'])
    
    mem_df['source_table'] = 'member'
    
    return mem_df


def predict_mem_role(mem_df):
    import pandas as pd
    import joblib
    from src.model.role_prediction import predict_role

    df = mem_df[['id', 'date', 'skill_list']]

    index = ['id', 'date']
    skills_list = 'skill_list'

    results = predict_role(df, index, skills_list)
    
    mem_pred_roles = pd.merge(mem_df, results, 
                                           on = ['id', 'date', 'skill_list'], 
                                           how = 'left')
    return mem_pred_roles


def process_mem_role_prediction(mem_pred_roles):
    import pandas as pd
    
    naive_member_role_model = pd.read_csv("data/reference/naive_member_role_model.csv")

    def role_selection(df):
        
        pass_value = df['pass']
        n_role = df['n_role']
        p_role = df['predicted_role']
        #confi = df['confidence']
        
        if pass_value == 0:
            if n_role == p_role:
                role =  n_role
                
            elif (n_role != '') == True:
                role =  n_role
            else:
                role =  p_role
        else:
            role =  ''
        
        return role
    
    
    mem_pred_roles['n_role'] = ''
    mem_pred_roles['pass'] = 0
    mem_pred_roles['role'] = ''
    
    mem_pred_roles['job_title'] = mem_pred_roles['job_title'].fillna('')
    
    for r in range(0, len(naive_member_role_model)):
        
        word = naive_member_role_model.loc[r, 'word'].strip()
        column = naive_member_role_model.loc[r, 'column']
        value = naive_member_role_model.loc[r, 'value']
        
        mem_pred_roles.loc[mem_pred_roles['job_title'].str.lower().str.contains(word), column] = value
    
    #mem_pred_roles.loc[mem_pred_roles['n_role'] == '', 'role'] = 'blank'
    
    mem_pred_roles['role'] = mem_pred_roles.apply(role_selection,  axis=1)
    
    mem_final_df = mem_pred_roles[['id', 'date', 'hourly_rate', 'salary', 
                                   'country', 'experience_level',
                    'skill_list', 'employment_type', 'source_table', 'role']]
    
    mem_final_df.to_csv("data/intermediate/mem_df_final.csv", index = False)
    
    print('Members Data Cleaned & Stored: data/intermediate/mem_df_final.csv')

def mem_salary_est(mem_df):
    import itertools
    import pandas as pd
    
    member_role_mapping = pd.read_csv("E:/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/reference/member_role_mapping.csv")
    member_role_mapping['employee_id'] = member_role_mapping['employee_id'].astype(str)
    mem_df['employee_id'] = mem_df['employee_id'].astype(str)
    
    mem_salary_data = pd.merge(mem_df, member_role_mapping[['employee_id', 'start_date', 'predicted_role']], 
                         on = ['employee_id', 'start_date'], 
                         how = 'left')
    combs = []
    mem_agg = pd.DataFrame()
    
    # combo level list
    agg_combo_list = ['country_clean', 'experience_level', 'emp_type', 
                      #'skill_list', 
                      'predicted_role']
    
    # All levels of salary to estimate
    
    for i in range(1, len(agg_combo_list)+1):
        els = [x for x in itertools.combinations(agg_combo_list, i)]
        combs = combs+els

    for c in combs:
        agg = mem_salary_data.groupby(list(c))['base_salary'].agg(['median', 'count']).reset_index()
    
        remaining_col = list(set(agg_combo_list) - set(c))
        
        for r in remaining_col:
            agg[r] = 'all'
    
        mem_agg = pd.concat([mem_agg, agg], axis=0)
        
    return mem_agg
    

# mem_df = combine_members_data()
# mem_pred_roles = predict_mem_role(mem_df)
# process_mem_role_prediction(mem_pred_roles)

















