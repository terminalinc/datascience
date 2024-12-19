SELECT
 *
FROM (
 SELECT
   DISTINCT candidate_id,
   created_at,
   updated_at,
   employment_type
 FROM
   product_database.candidate_id_lookup)
LEFT JOIN (
 SELECT
   candidate_id,
   country
 FROM
   product_database.candidate_location)
USING
 (candidate_id)
LEFT JOIN (
 SELECT
   candidate_id,
   status AS curation_workflow_status
 FROM
   product_database.candidate_curation_workflow
 WHERE
   is_latest_candidate_curation_workflow = TRUE)
USING
 (candidate_id)
LEFT JOIN (
 SELECT
   candidate_id,
   desired_salary_amount,
   desired_salary_currency,
   desired_salary_frequency,
   years_of_exp_range,
   contractor_rate,
   contractor_currency,
   contractor_payment_frequency
 FROM
   product_database.candidate_curation_detail)
USING
 (candidate_id)
LEFT JOIN (
 SELECT
   candidate_id,
   STRING_AGG(skill, '; '
   ORDER BY
     skill) AS skill_list
 FROM
   product_database.candidate_skill
 GROUP BY
   candidate_id)
USING
 (candidate_id)