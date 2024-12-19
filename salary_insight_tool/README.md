
**Instructions To Run Tool:**

- In a terminal, go into the Salary Insight Tools directory.
- Install the necessary packages contained within requirements.txt
- The *queries* folder contains all queries necessary to run the tool. Run the queries and export the result as csv into the respective folders under data/input. There are six queries that need to be run every time to get the latest salary data. 
- Before running the salary insight tool, the latest currency rates need to be pulled. Run `python update_currency_rates.py`. Note: this function uses a 3rd party API (exchangeratesapi.io) to pull the latest currency rates. You will require the Pro plan for this function to work. Place the API key here: "src\tool\constants.py", you can use the constants_template.py as an example to create this file.
- Once the input data & currency rates have been updated, to generate the salary estimates, run `python run_salary_insight_tool.py` 
- The tool will run for a few minutes and give updates at each stage. You can ignore any warning messages that occur as the tool runs. 
- The salary estimates will be outputted in the following directory: `data/output/salary_est.csv.`

**Troubleshooting:**
- If you receive an error message regarding missing files, insufficient rows or missing columns, check the following directories for any issues:
    -- `data/input/candidate_desired_salary.csv`
    -- `data/reference/usd_conversion_table.csv`
    -- `data/reference/country_conversion_table.csv`
