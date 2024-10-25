from src.preprocess.functions import * 
from src.analytics.functions import * 
from src.model.functions import * 
from src.health.functions import * 

def run_tool():
    import pandas as pd
    
    # Perform system check
    audit()
    
    # Load data
    cds_df = pd.read_csv('data/input/candidate_desired_salary.csv', low_memory=False)
    
    # Clean up and save Candidate Desired Salary data
    preprocess_cds_df(cds_df)
    
    # Flatten Candidate Desired Salary data
    skills_cds_df_flatten()
    
    # Identify top skills per role
    top_skills() 
    
    # Generate the salary estimates
    baseline_model()
    
if __name__ == '__main__':
    run_tool()