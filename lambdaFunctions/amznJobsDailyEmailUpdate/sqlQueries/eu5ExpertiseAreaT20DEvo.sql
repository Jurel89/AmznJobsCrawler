SELECT
	CASE 
		WHEN ddrd.job_category = 'Business Intelligence' THEN 'BIE'
		WHEN ddrd.job_category = 'Project/Program/Product Management--Technical' THEN 'PM-Tech'
		WHEN ddrd.job_category = 'Project/Program/Product Management--Non-Tech' THEN 'PM-NonTech'
		WHEN ddrd.job_category = 'Finance & Accounting' THEN 'Finance'
		WHEN ddrd.job_category = 'Buying, Planning, & Instock Management' THEN 'ISM'
		END as job_category
	, ddrd.snapshot_date
	, COUNT(DISTINCT ddrd.req_id) as opened_reqs

FROM 
	BOOKER.D_DAILY_REQ_DETAILS ddrd 
WHERE 
	ddrd.SNAPSHOT_DATE between DATE(NOW() - INTERVAL 20 DAY) AND DATE(NOW()) AND 
	ddrd.job_category in ('Business Intelligence','Project/Program/Product Management--Technical',
						'Project/Program/Product Management--Non-Tech','Finance & Accounting',
						'Buying, Planning, & Instock Management')
GROUP BY 1,2