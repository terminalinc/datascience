SELECT
 candidate_role.candidate_id,
 role_choices.name AS desired_role,
 candidate_role.years_of_exp AS desired_role_yoe
FROM
 product_database.candidate_role
LEFT JOIN
 product_database.role_choices
ON
 (candidate_role.role = role_choices.value)