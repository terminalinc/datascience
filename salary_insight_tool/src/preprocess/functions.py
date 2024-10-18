# data preprocessing related functions
def id_unique_values(df, index, calc_col):

    id_count = df.groupby(index).agg('count').reset_index()[[index, calc_col]]
    unique_values = list(id_count[id_count[calc_col] == 1][index])
    
    return(unique_values)
    
def id_missingdata_rows(df, index, col_list):
    
    missing_data_id = []

    for c in col_list:
        ids = df[df[c].isna()][index]
        missing_data_id = missing_data_id + (list(ids))
        
    return(list(set(missing_data_id)))

def annual_salary(row):
        if row['desired_salary_frequency'] == 'YEARLY':
            annual_salary = row['desired_salary_amount'] * row['usd_per_unit']
        
        elif row['desired_salary_frequency'] == 'MONTHLY':
            annual_salary = row['desired_salary_amount'] * row['usd_per_unit'] * 12
        else:
            annual_salary = 0
        return annual_salary
    
# Calculate interquartile range & Outlier values
def id_outlier_values(df, index, calc_col):
        import numpy as np
    
        q3, q1 = np.percentile(df[calc_col], [75 ,25])
        iqr = q3 - q1
    
        lower_outlier = q1 - (iqr*1.5)
        upper_outlier = q3 + (iqr*1.5)
    
        extreme_value_index = list(df[(df[calc_col]>upper_outlier) |
                                (df[calc_col]<lower_outlier)][index])
        
        return(extreme_value_index)
    
# Clean candidate desired salary data    
def preprocess_cds_df(cds_df):
    import pandas as pd
    
    usd_conv_df = pd.read_csv("data/reference/usd_conversion_table.csv") 
    ctry_conv_df = pd.read_csv("data/reference/country_conversion_table.csv") 

    # Convert all currency to USD & annual rates
    cds_df = cds_df.merge(usd_conv_df, on='desired_salary_currency', how= 'left')
    cds_df['annual_usd_salary'] = cds_df.apply(annual_salary, axis=1)
    
    # Clean Country Label
    cds_df.country = [str(v).strip() for v in cds_df.country]
    cds_df = cds_df.merge(ctry_conv_df, on='country', how= 'left')
    
    # Subset columns of interest
    cds_df = (cds_df[['candidate_id', 'created_at', 'updated_at', 'country_clean',
               'desired_salary_amount', 'desired_salary_currency', 'desired_salary_frequency', 
               'desired_role', 'years_of_exp_range', 'skill_list', 'annual_usd_salary']])
    
    # Exclude duplicate candidate IDs
    cds_df = (cds_df[cds_df['candidate_id']
                    .isin(id_unique_values(cds_df, 
                                           'candidate_id',
                                           'created_at'))])
    # Exclude candidate_ids with complete data
    cds_df = cds_df[~cds_df['candidate_id'] 
                    .isin(id_missingdata_rows(cds_df, 'candidate_id', list(cds_df.columns)))]

    # filter candidate ID to exclude outliers 
    cds_df = cds_df[~cds_df['candidate_id']
                    .isin(id_outlier_values(cds_df, 'candidate_id', 'annual_usd_salary'))]
    
    cds_df.to_csv('data/intermediate/clean_cds_df.csv', index = False)
    print('Candidate Salary Data cleaned and saved as data/intermediate/clean_cds_df.csv \n')

    
# Flatten & save Candidate Salary table to have single skill per row
def skills_cds_df_flatten():
    import pandas as pd
    
    clean_cds_df = pd.read_csv('data/intermediate/clean_cds_df.csv').reset_index(drop=True)
    flattened_cds_df = pd.DataFrame()

    for i in range(0, len(clean_cds_df)):
        
        ss_df = pd.DataFrame({'candidate_id': clean_cds_df['candidate_id'][i], 
                              'desired_role': clean_cds_df['desired_role'][i],
                              'country_clean': clean_cds_df['country_clean'][i],
                              'years_of_exp_range': clean_cds_df['years_of_exp_range'][i],
                              'annual_usd_salary': clean_cds_df['annual_usd_salary'][i],
                              'skill': clean_cds_df['skill_list'][i].split(';'), 
                              })
        flattened_cds_df = pd.concat([flattened_cds_df, ss_df], axis=0)

    flattened_cds_df.to_csv('data/intermediate/flattened_cds_df.csv', index = False)
    print('Candidate Salary Data flattened and saved as data/intermediate/flattened_cds_df.csv \n')
        