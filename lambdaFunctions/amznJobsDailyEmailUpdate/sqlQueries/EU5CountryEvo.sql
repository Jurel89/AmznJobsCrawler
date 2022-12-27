SELECT 
	COUNT(DISTINCT ddrd.req_id) as opened_reqs
	, ddrd.country_code 
	, ddrd.snapshot_date 
FROM 
	BOOKER.D_DAILY_REQ_DETAILS ddrd 
WHERE 
	ddrd .snapshot_date between DATE(NOW() - INTERVAL 8 DAY) AND DATE(NOW())
GROUP BY 2,3