SELECT 
	ddrd.req_id 
	, ddrd.req_description 
	, ddrd.company 
	, ddrd.business_category 
	, ddrd.location_description 
	, ddrd.created_date 
FROM 
	BOOKER.D_DAILY_REQ_DETAILS ddrd 
WHERE 
	UPPER(ddrd.job_category) like '%BUSINESS%INTELLIGENCE%' AND 
	ddrd.snapshot_date = DATE(NOW() - INTERVAL 1 DAY)
ORDER BY ddrd.created_date DESC