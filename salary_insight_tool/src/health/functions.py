# Identify top skills
def audit():
    import pandas as pd
    import sys
    
    try:
        cds_df = pd.read_csv("data/input/candidate_desired_salary.csv", low_memory=False)
        usd_conv_df = pd.read_csv("data/reference/usd_conversion_table.csv") 
        ctry_conv_df = pd.read_csv("data/reference/country_conversion_table.csv") 
    except:
        sys.exit('Key table(s) missing - Check system for essential files')
    
    # Check table lengths
    if len(cds_df) < 250000:
        sys.exit('Candidate Desired Salary table missing rows of data')
    
    if len(usd_conv_df) < 180:
        sys.exit('USD conversion table missing rows of data')
    
    if len(ctry_conv_df) < 120:
        sys.exit('Country conversion table missing rows of data')
    
    
    # Check for column names
    cds_columns = ['candidate_id', 'created_at', 'updated_at', 'country',
                   'desired_salary_amount', 'desired_salary_currency', 'desired_salary_frequency', 
                   'desired_role', 'years_of_exp_range', 'skill_list']
    if len(set(cds_columns) - set(cds_df.columns)) != 0:
        sys.exit('Candidate Desired Salary table missing key columns')
    

    usd_conv_columns = ['desired_salary_currency', 'currency_name', 'usd_per_unit', 'country_clean']
    if len(set(usd_conv_columns) - set(usd_conv_df.columns)) != 0:
        sys.exit('USD conversion table missing key columns')
        
    ctry_conv_columns = ['country', 'country_clean']
    if len(set(ctry_conv_columns) - set(ctry_conv_df.columns)) != 0:
        sys.exit('Country conversion table missing key columns')
    
    


