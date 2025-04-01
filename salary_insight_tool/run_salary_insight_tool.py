from src.preprocess.candidates import (id_new_candidate_ids, 
                                        process_cds_fulltime, 
                                        process_cds_contract, 
                                        process_candidate_data)
from src.preprocess.members import (combine_members_data, 
                                    predict_mem_role, 
                                    process_mem_role_prediction, 
                                    mem_salary_est)
from src.preprocess.jobs import (process_jobs_data)
from src.preprocess.combo_reference_df import (region_label, 
                                               create_salary_combo_df) 
from src.analytics.skill_analysis import *
from src.analytics.histogram_dist_generator import *
from src.prediction.true_salary_estimation import (compile_salary_results, 
                                                   salary_est)
from src.prediction.refine_salary_estimate import (refine_salary)
from src.prediction.salary_prediction import (salary_df_gen, 
                                              global_outlier_range, 
                                              construct_salary_model)
from src.analytics.agg_country_insight import agg_country
from src.analytics.agg_country_role_insight import agg_country_role
from src.analytics.agg_country_level_insight import agg_country_level


def run_tool():
    import pandas as pd
    
    # Clean up and save Candidate Desired Salary data
    id_new_candidate_ids()
    process_candidate_data()
    
    # Clean up and save Members Salary data
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
    
    # Agg salary insight
    agg_country_est = agg_country(salary_estimates_raw)
    agg_country_role_est = agg_country_role(salary_estimates_raw)
    agg_country_level_est = agg_country_level(salary_estimates_raw)
    
    # Generate salary histograms
    granular_salary = histogram_dist_generation(salary_estimates_raw)
    country_salary = histogram_dist_generation(agg_country_est)
    country_role_salary = histogram_dist_generation(agg_country_role_est)
    country_level_salary = histogram_dist_generation(agg_country_level_est)
    
    agg_salary_data = pd.concat([granular_salary, country_salary, country_role_salary, country_level_salary])
    
    agg_salary_data.to_csv('test.csv')
    
    # Combine and save salary results
    agg_salary_data.to_csv("data/output/salary_estimates.csv", index = False)
    print('Salary Estimates Stored: data/output/salary_estimates.csv')

    # Identify common & trending skills per role
    skills_analysis()
    
if __name__ == '__main__':
    run_tool()