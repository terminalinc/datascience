def skills_analysis():
    
    import pandas as pd
    from datetime import timedelta
    
    cds_df_final = pd.read_csv("data/intermediate/cds_df_final.csv")
    
    cds_df_final = cds_df_final[['date', 'role', 'skill_list']]
    
    cds_df_final['date'] = pd.to_datetime(cds_df_final["date"])
    
    date_d = cds_df_final.sort_values('date', ascending = False)['date'].reset_index(drop=True)[0]
    date_c = date_d - timedelta(days=180)
    date_b = date_c - timedelta(days=180)
    date_a = date_b - timedelta(days=180)
    
    window_a = cds_df_final[(cds_df_final['date'] > date_a) & (cds_df_final['date'] < date_b)]
    window_a = window_a.sort_values('date', ascending = True).reset_index(drop=True)
    window_a['skill_list'] = [str(s) for s in window_a['skill_list']]
    flattened_window_a = pd.DataFrame()
    
    for i in range(0, len(window_a)):
        ss_df = pd.DataFrame({'date': window_a['date'][i], 
                              'role': window_a['role'][i],
                              'skill': window_a['skill_list'][i].split(';'), 
                              })
        flattened_window_a = pd.concat([flattened_window_a, ss_df], axis=0)
        
    window_b = cds_df_final[(cds_df_final['date'] > date_b) & (cds_df_final['date'] < date_c)]
    window_b = window_b.sort_values('date', ascending = True).reset_index(drop=True)
    window_b['skill_list'] = [str(s) for s in window_b['skill_list']]
    flattened_window_b = pd.DataFrame()
    
    for i in range(0, len(window_b)):
        ss_df = pd.DataFrame({'date': window_b['date'][i], 
                              'role': window_b['role'][i],
                              'skill': window_b['skill_list'][i].split(';'), 
                              })
        flattened_window_b = pd.concat([flattened_window_b, ss_df], axis=0)
        
    window_c = cds_df_final[(cds_df_final['date'] > date_c) & (cds_df_final['date'] < date_d)]
    window_c = window_c.sort_values('date', ascending = True).reset_index(drop=True)
    window_c['skill_list'] = [str(s) for s in window_c['skill_list']]
    flattened_window_c = pd.DataFrame()
    
    for i in range(0, len(window_c)):
        ss_df = pd.DataFrame({'date': window_c['date'][i], 
                              'role': window_c['role'][i],
                              'skill': window_c['skill_list'][i].split(';'), 
                              })
        flattened_window_c = pd.concat([flattened_window_c, ss_df], axis=0)
    
    flattened_window_a['skill'] = [s.strip() for s in flattened_window_a['skill']]
    window_a_agg = flattened_window_a.groupby(['role', 'skill']).agg('count').reset_index()
    window_a_agg.columns = ['role', 'skill', 'count_a']
    
    flattened_window_b['skill'] = [s.strip() for s in flattened_window_b['skill']]
    window_b_agg = flattened_window_b.groupby(['role', 'skill']).agg('count').reset_index()
    window_b_agg.columns = ['role', 'skill', 'count_b']
    
    flattened_window_c['skill'] = [s.strip() for s in flattened_window_c['skill']]
    window_c_agg = flattened_window_c.groupby(['role', 'skill']).agg('count').reset_index()
    window_c_agg.columns = ['role', 'skill', 'count_c']
    
    skill_df = window_a_agg.merge(window_b_agg, on = ['role', 'skill'], how = 'outer')
    skill_df = skill_df.merge(window_c_agg, on = ['role', 'skill'], how = 'outer')
    
    skill_df['count_a'] = skill_df['count_a'].fillna(0)
    skill_df['count_b'] = skill_df['count_b'].fillna(0)
    skill_df['count_c'] = skill_df['count_c'].fillna(0)
    
    skill_df['total_count'] = skill_df['count_a'] + skill_df['count_b'] + skill_df['count_c']
    
    skill_df['diff_a'] = (skill_df['count_b'] - skill_df['count_a']) / skill_df['count_a']
    skill_df['diff_b'] = (skill_df['count_c'] - skill_df['count_b']) / skill_df['count_b']
    
    skill_df['count_rank'] = (skill_df.groupby('role')['total_count']
                          .rank(method='first', ascending=False)
                          .astype(int))
    
    common_skills = skill_df[skill_df['count_rank']<11]
    common_skills = common_skills[['role', 'skill', 'count_rank']]
    
    trending_skills = skill_df[(skill_df['diff_a'] > 0) 
                               & (skill_df['diff_b'] > 0)
                               & (skill_df['count_rank'] > 10)]
    
    trending_skills['count_rank'] = (trending_skills.groupby('role')['total_count']
                          .rank(method='first', ascending=False)
                          .astype(int))
    trending_skills = trending_skills[trending_skills['count_rank']<6]
    trending_skills = trending_skills[['role', 'skill', 'count_rank']]
    
    trending_skills.to_csv("data/output/trending_skills.csv", index = False)
    common_skills.to_csv("data/output/common_skills.csv", index = False)
    
    print('Common & Trending skills stored: data/output')



