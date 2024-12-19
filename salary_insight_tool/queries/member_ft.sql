SELECT
 EmploymentStatuses.employeeXRefCode,
 EmploymentStatuses.EffectiveStart,
 EmploymentStatuses.EffectiveEnd,
 EmploymentStatus_XRefCode AS status,
 EmploymentStatusReason_XRefCode AS status_reason,
 BaseRate,
 BaseSalary,
 country_code,
 level,
 work_assignment_by_date.WorkAssignments.Position_Department_ShortName AS department,
 work_assignment_by_date.WorkAssignments.Position_Job_ShortName AS job_title,
 skill_list
FROM
 dayforce.EmploymentStatuses
LEFT JOIN (
 SELECT
   employeeXRefCode,
   Country_XRefCode AS country_code,
   ROW_NUMBER() OVER(PARTITION BY employeeXRefCode ORDER BY EffectiveStart DESC) AS row_num
 FROM
   dayforce.Addresses
 WHERE
   ContactInformationType_XRefCode = 'PrimaryResidence'
 QUALIFY
   row_num = 1)
USING
 (employeeXRefCode)
LEFT JOIN (
 SELECT
   employeeXRefCode,
   OptionValue_XRefCode AS level,
   ROW_NUMBER() OVER(PARTITION BY employeeXRefCode ORDER BY COALESCE(EffectiveEnd, EffectiveStart) DESC) AS row_num
 FROM
   dayforce.EmployeeProperties
 WHERE
   EmployeeProperty_ShortName IN ('Level')
 QUALIFY
   row_num = 1)
USING
 (employeeXRefCode)
LEFT JOIN (
 SELECT
   DISTINCT employeeXRefCode,
   skill_list
 FROM (
   SELECT
     employeeXRefCode,
     SAFE_CAST(StringValue AS INT64) AS icims_person_id,
     ROW_NUMBER() OVER(PARTITION BY employeeXRefCode ORDER BY LastModifiedTimestamp DESC) AS row_num
   FROM
     dayforce.EmployeeProperties
   WHERE
     EmployeeProperty_ShortName = 'iCIMS Person ID'
   QUALIFY
     row_num = 1)
 LEFT JOIN
   etl_util.util_candidate
 USING
   (icims_person_id)
 LEFT JOIN (
   SELECT
     candidate_id AS prod_candidate_id,
     STRING_AGG(skill, '; '
     ORDER BY
       skill) AS skill_list
   FROM
     product_database.candidate_skill
   GROUP BY
     candidate_id)
 USING
   (prod_candidate_id))
USING
 (employeeXRefCode)
LEFT JOIN
 dayforce.work_assignment_by_date
ON
 (EmploymentStatuses.employeeXRefCode = work_assignment_by_date.employeeXRefCode
   AND DATE(EmploymentStatuses.EffectiveStart) = work_assignment_by_date.date)
WHERE
 PayClass_XRefCode IN ('FT')
 AND EmploymentStatus_XRefCode NOT IN ('PRESTART',
   'INACTIVE')
ORDER BY
 employeeXRefCode,
 EffectiveStart,
 EffectiveEnd