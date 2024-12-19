SELECT
 *
FROM (
 SELECT
   job.id AS job_id,
   job.created_at,
   role_choices.name AS role_name,
   job.level,
   job.min_years_of_experience,
   job.min_salary,
   job.max_salary,
   job.min_contract_rate,
   job.max_contract_rate,
   COALESCE(job.employment_type, 'FULL_TIME') AS employment_type
 FROM
   product_database.job
 LEFT JOIN
   product_database.organization
 ON
   (job.organization_id = organization.id)
 LEFT JOIN
   product_database.role_choices
 ON
   (job.role_type = role_choices.value)
 WHERE
   NOT(REGEXP_CONTAINS(LOWER(organization.name),"demo|test")))
LEFT JOIN (
 SELECT
   job_id,
   latam_min_salary,
   latam_max_salary,
   canada_min_salary,
   canada_max_salary,
   europe_min_salary,
   europe_max_salary,
   latam_min_contractor_rate,
   latam_max_contractor_rate,
   canada_min_contractor_rate,
   canada_max_contractor_rate,
   europe_min_contractor_rate,
   europe_max_contractor_rate
 FROM
   product_database.job_meta_info)
USING
 (job_id)
LEFT JOIN (
 SELECT
   job_acceptable_location.job_id,
   STRING_AGG(location.value, '; '
   ORDER BY
     location.value) AS location_list
 FROM
   product_database.job_acceptable_location
 LEFT JOIN
   product_database.location
 ON
   (job_acceptable_location.location_id = location.id)
 GROUP BY
   job_acceptable_location.job_id)
USING
 (job_id)
LEFT JOIN (
 SELECT
   job_required_skill.job_id,
   STRING_AGG(skill.name
   ORDER BY
     skill.name) AS required_skills
 FROM
   product_database.job_required_skill
 LEFT JOIN
   product_database.skill
 ON
   (job_required_skill.skill_id = skill.id)
 GROUP BY
   job_required_skill.job_id)
USING
 (job_id)
LEFT JOIN (
 SELECT
   job_nice_to_have_skill.job_id,
   STRING_AGG(skill.name
   ORDER BY
     skill.name) AS nice_to_have_skills
 FROM
   product_database.job_nice_to_have_skill
 LEFT JOIN
   product_database.skill
 ON
   (job_nice_to_have_skill.skill_id = skill.id)
 GROUP BY
   job_nice_to_have_skill.job_id)
USING
 (job_id)
LEFT JOIN (
 SELECT
   job_id,
   COUNT(*) AS job_position_count
 FROM
   product_database.job_position
 GROUP BY
   job_id)
USING
 (job_id)
WHERE
 employment_type IN ('CONTRACT')
ORDER BY
 created_at