-- Intended to run in BigQuery.
SELECT
    *
EXCEPT
(row_num)
FROM
    (
        SELECT
            employeeXRefCode,
            COALESCE(EffectiveEnd, EffectiveStart) AS date,
            BaseRate,
            BaseSalary,
            ROW_NUMBER() OVER (
                PARTITION BY
                    employeeXRefCode
                ORDER BY
                    COALESCE(EffectiveEnd, EffectiveStart) DESC
            ) AS row_num,
        FROM
            dayforce.EmploymentStatuses
        WHERE
            PayClass_XRefCode IN ('FT') QUALIFY row_num = 1
    )
    LEFT JOIN (
        SELECT
            employeeXRefCode,
            Country_XRefCode AS country,
            ROW_NUMBER() OVER (
                PARTITION BY
                    employeeXRefCode
                ORDER BY
                    COALESCE(EffectiveEnd, EffectiveStart) DESC
            ) AS row_num,
        FROM
            dayforce.Addresses QUALIFY row_num = 1
    ) USING (employeeXRefCode)
    LEFT JOIN (
        SELECT
            employeeXRefCode,
            OptionValue_XRefCode AS level,
            ROW_NUMBER() OVER (
                PARTITION BY
                    employeeXRefCode
                ORDER BY
                    COALESCE(EffectiveEnd, EffectiveStart) DESC
            ) AS row_num
        FROM
            dayforce.EmployeeProperties
        WHERE
            EmployeeProperty_ShortName IN ('Level') QUALIFY row_num = 1
    ) USING (employeeXRefCode)
    LEFT JOIN (
        SELECT
            employeeXRefCode,
            skill_list
        FROM
            (
                SELECT
                    employeeXRefCode,
                    SAFE_CAST (StringValue AS INT64) AS icims_person_id,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            employeeXRefCode
                        ORDER BY
                            LastModifiedTimestamp DESC
                    ) AS row_num
                FROM
                    dayforce.EmployeeProperties
                WHERE
                    EmployeeProperty_ShortName = 'iCIMS Person ID' QUALIFY row_num = 1
            )
            LEFT JOIN etl_util.util_candidate USING (icims_person_id)
            LEFT JOIN (
                SELECT
                    candidate_id AS prod_candidate_id,
                    STRING_AGG (
                        skill,
                        '; '
                        ORDER BY
                            skill
                    ) AS skill_list
                FROM
                    product_database.candidate_skill
                GROUP BY
                    candidate_id
            ) USING (prod_candidate_id)
    ) USING (employeeXRefCode)
    LEFT JOIN (
        SELECT
            *
        EXCEPT
        (row_num)
        FROM
            (
                SELECT
                    dayforce_all_member.employeeXRefCode,
                    COALESCE(
                        offer.offer.offer_job_title,
                        dayforce_all_member.Position_Job_ShortName
                    ) AS job_title,
                    offer.offer.offer_type AS offer_type,
                    ROW_NUMBER() OVER (
                        PARTITION BY
                            dayforce_all_member.employeeXRefCode,
                            dayforce_all_member.start_date
                        ORDER BY
                            ABS(
                                DATE_DIFF (
                                    dayforce_all_member.start_date,
                                    DATE (offer.offer.offer_proposed_start_date),
                                    DAY
                                )
                            )
                    ) AS row_num,
                FROM
                    etl_util.dayforce_all_member
                    LEFT JOIN (
                        SELECT
                            offer,
                            icims_applicant_person_job_client
                        FROM
                            latest.offer
                            LEFT JOIN etl_util.icims_applicant_person_job_client ON (
                                SAFE_CAST (offer.icims_applicant_id AS INT64) = icims_applicant_person_job_client.icims_applicant_id
                            )
                    ) AS offer ON (
                        dayforce_all_member.icims_person_id = offer.offer.icims_person_id
                        AND dayforce_all_member.client_id = offer.icims_applicant_person_job_client.client_id
                    ) QUALIFY row_num = 1
            )
    ) USING (employeeXRefCode)