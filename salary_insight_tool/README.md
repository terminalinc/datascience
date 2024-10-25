**Instructions To Run Tool:**

- In a terminal, go into the Salary Insight Tools directory.
- Enter the virtual environment: `venv\Scripts\activate.bat`.
- Place all of the candidate desired salary into the following directory: `data/input/candidate_desired_salary.csv.`
- To generate the salary estimates, run `python run.py` 
- The tool will run for a few minutes and give updates at each stage.
- The salary estimates will be outputted in the following directory: `data/output/salary_est_{timestamp}.csv.`


**Troubleshooting:**
- If you receive an error message regarding missing files, insufficient rows or missing columns, check the following directories for any issues:
    -- `data/input/candidate_desired_salary.csv`
    -- `data/reference/usd_conversion_table.csv`
    -- `data/reference/country_conversion_table.csv`
