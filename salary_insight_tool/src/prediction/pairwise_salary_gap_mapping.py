import pandas as pd

mem_final_df = pd.read_csv("/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/intermediate/mem_df_final.csv")
job_final_df = pd.read_csv("/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/intermediate/job_df_final.csv")
cds_df_final = pd.read_csv("/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/intermediate/cds_df_final.csv")
experience_level = pd.read_csv("/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/reference/experience_level.csv")
tpd_df = pd.read_csv("E:/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/reference/3rd_party_data.csv") 

salary_df_nonencoded = mem_final_df.copy()#salary_df_gen()[1]

job_final_df.columns

col = 'level'

r = list(salary_df_nonencoded[col].unique())
r = [v for v in r if str(v) not in ['0', 'nan']]

r_df = pd.DataFrame(itertools.product(r, r))
r_df.columns = ['ref', 'comp']
r_df['column'] = col
r_df['match'] = np.where(r_df['ref'] == r_df['comp'], 1, 0)
r_df = r_df[r_df['match'] == 0][['ref', 'comp', 'column']]

salary_combo_dict = {}

for v in r:
    s = salary_df_nonencoded[salary_df_nonencoded[col] == v]['salary']
    print(s)
    
    if len(s) > 4: 
        bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                , n_resamples = 5000, method='basic')
        
        salary_lower_s = bootstrap_s.confidence_interval[0]
        salary_upper_s = bootstrap_s.confidence_interval[1]
        salary_median_s = (salary_lower_s + salary_upper_s)/2
        
        salary_combo_dict[v] = salary_median_s
    else:
        salary_combo_dict[v] = np.median(s)
            
    
r_df['ref_salary'] = [salary_combo_dict[v] for v in r_df['ref']]
r_df['comp_salary'] = [salary_combo_dict[v] for v in r_df['comp']]

r_df['per_diff'] = (r_df['comp_salary'] - r_df['ref_salary']) / r_df['ref_salary']

r_df.to_csv('temp.csv')

# 11130.621044702433 w/ 
# 11764.505945620753 with Job yoe
# 16k w/ jobs roles
# 25k w/ cds roles
# no difference - jobs levels
# mem levels - adjusted L6
#### Adjust salary values
ref_df = pd.read_csv("/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/reference/pairewise_salary_gap_mapping.csv")

salary_non_adjusted = salary_estimates_raw[['country', 'role', 'level', 'employment_type', 'yoe', 'job_level', 'M']]

trd_index = list(salary_estimates_raw[~(salary_estimates_raw['median_salary'].isna())].index)

for k in trd_index:

    print(k)
    
    d = salary_estimates_ss.iloc[k,:]
    cv = d['country']
    rv = d['role']
    yv = d['yoe']
    jv = d['job_level']
    tv = d['employment_type']
    lv = d['level']
    
    sv = d['M']
    
    comp_ss = ref_df[ref_df['ref'].isin([cv, rv, yv])].reset_index(drop=True) #jv, tv, lv
    
    if len(comp_ss) > 0:
        comp_ss.loc[:, 'actual_ref_salary'] = sv
        
        for i in range(0, len(comp_ss)):
            col_name = comp_ss.loc[i, 'column']
            col_value = comp_ss.loc[i, 'comp']
                        
            if col_name == 'role':
                acs = salary_non_adjusted[(salary_non_adjusted['country'] == cv)
                                    & (salary_non_adjusted['role'] == col_value)
                                    & (salary_non_adjusted['yoe'] == yv)
                                    & (salary_non_adjusted['job_level'] == jv)
                                    & (salary_non_adjusted['level'] == lv)
                                    & (salary_non_adjusted['employment_type'] == tv)]
                if len(acs)>0:
                    acs = acs['M'].reset_index(drop=True)[0]
                
            elif col_name == 'country':
                acs = salary_non_adjusted[(salary_non_adjusted['country'] == col_value)
                                    & (salary_non_adjusted['role'] == rv)
                                    & (salary_non_adjusted['yoe'] == yv)
                                    & (salary_non_adjusted['job_level'] == jv)
                                    & (salary_non_adjusted['level'] == lv)
                                    & (salary_non_adjusted['employment_type'] == tv)]
                if len(acs)>0:
                    acs = acs['M'].reset_index(drop=True)[0]
                            
                
            elif col_name == 'yoe':
                acs = salary_non_adjusted[(salary_non_adjusted['country'] == cv)
                                    & (salary_non_adjusted['role'] == rv)
                                    & (salary_non_adjusted['yoe'] == col_value)
                                    & (salary_non_adjusted['job_level'] == jv)
                                    & (salary_non_adjusted['level'] == lv)
                                    & (salary_non_adjusted['employment_type'] == tv)]
                if len(acs)>0:
                    acs = acs['M'].reset_index(drop=True)[0]
                
            elif col_name == 'level':
                acs = salary_non_adjusted[(salary_non_adjusted['country'] == cv)
                                    & (salary_non_adjusted['role'] == rv)
                                    & (salary_non_adjusted['yoe'] == yv)
                                    & (salary_non_adjusted['job_level'] == jl)
                                    & (salary_non_adjusted['level'] == col_value)
                                    & (salary_non_adjusted['employment_type'] == tv)]
                if len(acs)>0:
                    acs = acs['M'].reset_index(drop=True)[0]
                
            # elif col_name == 'job_level':
            #     acs = salary_non_adjusted[(salary_non_adjusted['country'] == cv)
            #                         & (salary_non_adjusted['role'] == rv)
            #                         & (salary_non_adjusted['yoe'] == yv)
            #                         & (salary_non_adjusted['job_level'] == col_value)
            #                         & (salary_non_adjusted['level'] == lv)
            #                         & (salary_non_adjusted['employment_type'] == tv)]
            #     if len(acs)>0:
            #         acs = acs['M'].reset_index(drop=True)[0]
                
            elif col_name == 'employment_type':
                acs = salary_non_adjusted[(salary_non_adjusted['country'] == cv)
                                    & (salary_non_adjusted['role'] == rv)
                                    & (salary_non_adjusted['yoe'] == yv)
                                    & (salary_non_adjusted['job_level'] == jv)
                                    & (salary_non_adjusted['level'] == lv)
                                    & (salary_non_adjusted['employment_type'] == col_value)]
                if len(acs)>0:
                    acs = acs['M'].reset_index(drop=True)[0]
                
            comp_ss.loc[i:, 'actual_comp_salary'] = acs
            
        comp_ss['actual_per_diff'] = (comp_ss['actual_comp_salary'] - comp_ss['actual_ref_salary']) / comp_ss['actual_ref_salary']
        
        comp_ss_nona = comp_ss[~(comp_ss['actual_per_diff'].isna())]
        
        percent_change = (1 + np.median(comp_ss_nona['actual_per_diff'] - comp_ss_nona['per_diff']))
        adjusted_M = sv * percent_change
        
        salary_non_adjusted.loc[k, 'percent_change'] = percent_change
        salary_non_adjusted.loc[k, 'adjusted_M'] = adjusted_M

results = salary_estimates_raw.merge(salary_non_adjusted, 
                on = ['country', 'role', 'level', 'employment_type', 'yoe', 'job_level', 'M'], 
                how = 'left')

results_ss = results[~(results['median_salary'].isna())]
results_ss['abs_diff'] = abs(results_ss['median_salary'] - results_ss['adjusted_M'])
print(np.mean(results_ss['abs_diff']))

results_ss.to_csv('temp.csv')

results.columns
#### Wider level based comparison


#####
mem_final_df.groupby('experience_level')['salary'].agg('mean')
l = ['L2', 'L3','L4', 'L5', 'L6']

for i in l:
    s = mem_final_df[mem_final_df['experience_level'] == i]['salary']
    
    q3, q1 = np.percentile(s, [75 ,25])
    iqr = q3 - q1
    
    lower_outlier = q1 - (iqr*2)
    upper_outlier = q3 + (iqr*2)
    
    s_new = [i for i in s if  i > lower_outlier and i <upper_outlier]
    print(np.mean(s_new))
    
    
    
cds_df_final.columns
import itertools

job_final_df.columns


        

ref_comp_df = pd.DataFrame(itertools.product(e_dict.keys(), e_dict.keys()))
ref_comp_df.columns = ['ref', 'comp']

ref_comp_df.to_csv('temp4.csv')

tpd_values = ref_comp_df.copy()
tpd_values.to_csv('temp3.csv')

.groupby('experience_level')[['median_salary', 'salary_low', 'salary_high']].agg('mean').reset_index().to_csv('temp1.csv')
'TWO_FIVE'

### Old
salary_combo_dict = {}
r = list(tpd_df.role.unique())
c = list(tpd_df.country.unique())
e = list(tpd_df.experience_level.unique())

for i in r:
    print(i)
    d = tpd_df[tpd_df['role']==i]
    s = (list(d['median_salary']) + list(d['salary_low']) + list(d['salary_high']))
    #s = d['salary']
    
    if len(s) > 4: 
        bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                , n_resamples = 5000, method='basic')
        
        salary_lower_s = bootstrap_s.confidence_interval[0]
        salary_upper_s = bootstrap_s.confidence_interval[1]
        salary_median_s = (salary_lower_s + salary_upper_s)/2
        
        salary_combo_dict[i] = salary_median_s
    else:
        salary_combo_dict[i] = np.median(s)
        
for i in c:
    print(i)
    d = tpd_df[tpd_df['country']==i]
    s = (list(d['median_salary']) + list(d['salary_low']) + list(d['salary_high']))
    #s = d['salary']
    
    if len(s) > 4: 
        bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                , n_resamples = 5000, method='basic')
        
        salary_lower_s = bootstrap_s.confidence_interval[0]
        salary_upper_s = bootstrap_s.confidence_interval[1]
        salary_median_s = (salary_lower_s + salary_upper_s)/2
        
        salary_combo_dict[i] = salary_median_s
    else:
        salary_combo_dict[i] = np.median(s)

for i in e:
    print(i)
    d = tpd_df[tpd_df['experience_level']==i]
    s = (list(d['median_salary']) + list(d['salary_low']) + list(d['salary_high']))
    #s = d['salary']
    
    if len(s) > 4: 
        bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                , n_resamples = 5000, method='basic')
        
        salary_lower_s = bootstrap_s.confidence_interval[0]
        salary_upper_s = bootstrap_s.confidence_interval[1]
        salary_median_s = (salary_lower_s + salary_upper_s)/2
        
        salary_combo_dict[i] = salary_median_s
    else:
        salary_combo_dict[i] = np.median(s)
        
r_df = pd.DataFrame(itertools.product(r, r))
r_df.columns = ['ref', 'comp']
r_df['column'] = 'role'

c_df = pd.DataFrame(itertools.product(c, c))
c_df.columns = ['ref', 'comp']
c_df['column'] = 'country'

e_df = pd.DataFrame(itertools.product(e, e))
e_df.columns = ['ref', 'comp']
e_df['column'] = 'experience_level'

ref_df = pd.concat([r_df, c_df, e_df], axis = 0)
ref_df['match'] = np.where(ref_df['ref'] == ref_df['comp'], 1, 0)
ref_df = ref_df[ref_df['match'] == 0][['ref', 'comp', 'column']]

ref_df['ref_salary'] = [salary_combo_dict[v] for v in ref_df['ref']]
ref_df['comp_salary'] = [salary_combo_dict[v] for v in ref_df['comp']]

ref_df['per_diff'] = (ref_df['comp_salary'] - ref_df['ref_salary']) / ref_df['ref_salary']
ref_df.to_csv('ref_df.csv')

### OLD
gor = pd.read_csv('E:/Sync/3_Professional/Terminal_Sync/datascience/salary_insight_tool/data/reference/global_outlier_range.csv')
salary_df_ss = salary_df_nonencoded[(salary_df_nonencoded['salary'] < gor['global_upper_bound'][0]) 
                      & (salary_df_nonencoded['salary']> gor['global_lower_bound'][0])]

r = list(salary_df_ss.role.unique())
r = [v for v in r if str(v) not in ['0', 'nan']]

r_df = pd.DataFrame(itertools.product(r, r))
r_df.columns = ['ref', 'comp']
r_df['column'] = 'role'

c = list(salary_df_ss.country.unique())
c = [v for v in c if str(v) not in ['0', 'nan']]

c_df = pd.DataFrame(itertools.product(c, c))
c_df.columns = ['ref', 'comp']
c_df['column'] = 'country'

y = list(salary_df_ss.yoe.unique())
y = [v for v in y if str(v) not in ['0', 'nan']]

y_df = pd.DataFrame(itertools.product(y, y))
y_df.columns = ['ref', 'comp']
y_df['column'] = 'yoe'

j = list(salary_df_ss.job_level.unique())
j = [v for v in j if str(v) not in ['0', 'nan']]

j_df = pd.DataFrame(itertools.product(j, j))
j_df.columns = ['ref', 'comp']
j_df['column'] = 'job_level'

t = list(salary_df_ss.employment_type.unique())
t = [v for v in t if str(v) not in ['0', 'nan']]

t_df = pd.DataFrame(itertools.product(t, t))
t_df.columns = ['ref', 'comp']
t_df['column'] = 'employment_type'

l = list(salary_df_ss.level.unique())
l = [v for v in l if str(v) not in ['0', 'nan']]

l_df = pd.DataFrame(itertools.product(l, l))
l_df.columns = ['ref', 'comp']
l_df['column'] = 'level'

column_dict = {'role':r, 'country': c, 
               'yoe': y, 'job_level': j, 
               'employment_type': t, 
               'level': l}

ref_df = pd.concat([r_df, c_df, y_df, j_df, t_df, l_df], axis = 0)
ref_df['match'] = np.where(ref_df['ref'] == ref_df['comp'], 1, 0)
ref_df = ref_df[ref_df['match'] == 0][['ref', 'comp', 'column']]

salary_combo_dict = {}

for c in column_dict.keys():
    for v in column_dict[c]:
        s = salary_df_ss[salary_df_ss[c] == v]['salary']
        print(v)
        
        if len(s) > 4: 
            bootstrap_s = bootstrap((s,), np.median, confidence_level=0.95
                                    , n_resamples = 5000, method='basic')
            
            salary_lower_s = bootstrap_s.confidence_interval[0]
            salary_upper_s = bootstrap_s.confidence_interval[1]
            salary_median_s = (salary_lower_s + salary_upper_s)/2
            
            salary_combo_dict[v] = salary_median_s
        else:
            salary_combo_dict[v] = np.median(s)
            
    
ref_df['ref_salary'] = [salary_combo_dict[v] for v in ref_df['ref']]
ref_df['comp_salary'] = [salary_combo_dict[v] for v in ref_df['comp']]

ref_df['per_diff'] = (ref_df['comp_salary'] - ref_df['ref_salary']) / ref_df['ref_salary']

ref_df.to_csv('temp12.csv')