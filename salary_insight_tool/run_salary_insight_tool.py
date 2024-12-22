from src.preprocess.candidates import * 
from src.preprocess.members import * 
from src.preprocess.jobs import * 
from src.preprocess.combo_reference_df import * 
from src.analytics.skill_analysis import *
from src.analytics.histogram_dist_generator import *
from src.prediction.true_salary_estimation import *
from src.prediction.refine_salary_estimate import *
from src.prediction.salary_prediction import *

def run_tool():
    import pandas as pd
    
    # # Clean up and save Candidate Desired Salary data
    id_new_candidate_ids()
    process_candidate_data()
    
    # # Clean up and save Members Salary data
    mem_df = combine_members_data()
    mem_pred_roles = predict_mem_role(mem_df)
    process_mem_role_prediction(mem_pred_roles)
    
    # Clean up and save Jobs Salary data
    process_jobs_data()
    
    # Construct reference combo table
    create_salary_combo_df() 
    
    # Construct salary prediction model
    salary_df = salary_df_gen()[0]
    global_outlier_range(salary_df)
    construct_salary_model(salary_df)
    
    # Generate the salary estimates
    salary_estimates_raw = compile_salary_results()
    salary_estimates_raw[['M', 'figure_data', 'n', 'confidence']] = salary_estimates_raw.apply(salary_est, axis = 1, result_type='expand')    
        
    # Refine Salary Estimates
    salary_estimates_raw = refine_salary(salary_estimates_raw)
    
    # Generate salary histograms
    histogram_dist_generation(salary_estimates_raw)
    
    # # Identify common & trending skills per role
    skills_analysis()
    
if __name__ == '__main__':
    run_tool()