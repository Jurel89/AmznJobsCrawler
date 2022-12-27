SELECT 
	ddrd.req_id 
	, ddrd.req_description 
	, ddrd.company 
	, ddrd.business_category 
	, ddrd.location_description 
	, ddrd.update_since 
	, ddrd.created_date 
FROM 
	BOOKER.D_DAILY_REQ_DETAILS ddrd 
WHERE 
	ddrd.snapshot_date in (SELECT max(snapshot_date) FROM BOOKER.D_DAILY_REQ_DETAILS) AND 
	ddrd .created_date between DATE(NOW() - INTERVAL 7 DAY) AND DATE(NOW())
ORDER BY ddrd.created_date DESC
LIMIT 20