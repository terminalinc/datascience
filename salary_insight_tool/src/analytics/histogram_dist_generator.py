def transform_hist_data(row):
    import pandas as pd
    import numpy as np

    figure_data = pd.Series(row['figure_data'])
    og_median = np.median(figure_data)
    
    target_median = row['M']
    modifier = 1 + (target_median - og_median) / og_median
    transformed_data =  list(figure_data * modifier)
    
    return transformed_data


def histogram_dist_generation(salary_estimates_raw):
    import pandas as pd
      
    gor = pd.read_csv("data/reference/global_outlier_range.csv")

    # Create & store histogram buckets
    lb_a = gor['global_lower_bound'][0]
    ub_d = gor['global_upper_bound'][0]
    middle = (lb_a + ub_d)/2
    lb_c = (lb_a + middle)/2
    ub_b = (ub_d + middle)/2
    lb_b = (lb_a + lb_c)/2
    lb_d = (lb_c + middle)/2
    ub_a = (ub_b + middle)/2
    ub_c = (ub_b + ub_d)/2
    
    hist_bin_name = ['hist_bin_1', 'hist_bin_2', 'hist_bin_3', 'hist_bin_4', 
                    'hist_bin_5', 'hist_bin_6', 'hist_bin_7', 'hist_bin_8']
    hist_bin_range = [[lb_a, lb_b], [lb_b, lb_c], [lb_c, lb_d], [lb_d, middle], 
                      [middle, ub_a], [ub_a, ub_b], [ub_b, ub_c], [ub_c, ub_d]]
    hist_bin_data = pd.DataFrame({'hist_bin_name': hist_bin_name, 'hist_bin_range':hist_bin_range})
    
    hist_bin_data.to_csv("data/output/hist_bin_data.csv", index = False)

    salary_estimates_raw['transformed_data'] = salary_estimates_raw.apply(transform_hist_data, axis = 1)
    
    
    salary_estimates_raw['hist_bin_1'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > lb_a) & (x <= lb_b), y)))))
    
    salary_estimates_raw['hist_bin_2'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > lb_b) & (x <= lb_c), y)))))
    
    salary_estimates_raw['hist_bin_3'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > lb_c) & (x <= lb_d), y)))))
    
    salary_estimates_raw['hist_bin_4'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > lb_d) & (x <= middle), y)))))
    
    salary_estimates_raw['hist_bin_5'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > middle) & (x <= ub_a), y)))))
    
    salary_estimates_raw['hist_bin_6'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > ub_a) & (x <= ub_b), y)))))
    
    salary_estimates_raw['hist_bin_7'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > ub_b) & (x <= ub_c), y)))))
    
    salary_estimates_raw['hist_bin_8'] = (salary_estimates_raw['transformed_data']
                                          .apply(lambda y : len(list(filter(
                                              lambda x : (x > ub_c) & (x <= ub_d), y)))))
    
    salary_estimates_raw['total'] = (salary_estimates_raw['cds_n']
                                     + salary_estimates_raw['job_n']
                                     + salary_estimates_raw['mem_n'])
    
    salary_estimates_raw.to_csv("data/output/salary_estimates.csv", index = False)
    print('Salary Estimates Stored: data/output/salary_estimates.csv')


