# Identify top skills
def top_skills():
    import pandas as pd
    
    cds_ref = pd.read_csv('data/intermediate/flattened_cds_df.csv')
    
    skill_role_freq = (cds_ref.groupby(['desired_role', 'skill']).agg('count')
                        .reset_index()[['desired_role', 'skill', 'country_clean']])
    skill_role_freq.columns = ['desired_role', 'skill', 'count']
    
    # Window function to determin top skills in decending order
    skill_role_freq['top_n_skills'] = (skill_role_freq.groupby([ 'desired_role'])['count']
                                          .rank(method='first', ascending=False)
                                          .astype(int))
    
    role_skill_list = (skill_role_freq[skill_role_freq['top_n_skills'] < 11]
                        .sort_values('top_n_skills', ascending = True)
                        [['desired_role', 'skill']])
    
    role_skill_list['top_skill'] = 1
    
    role_skill_list.to_csv('data/intermediate/role_skill_list.csv', index = False)
    
    print('Top skills per role found and saved as data/intermediate/role_skill_list.csv \n')

