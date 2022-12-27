SELECT
	ddrd.country_code
	, ddrd.snapshot_date
	, COUNT(DISTINCT ddrd.req_id) as opened_reqs
FROM 
	BOOKER.D_DAILY_REQ_DETAILS ddrd 
WHERE 
	ddrd.SNAPSHOT_DATE between DATE(NOW() - INTERVAL 20 DAY) AND DATE(NOW()) AND 
	ddrd.country_code in ('ESP','ITA','FRA','DEU','GBR','LUX')
GROUP BY 1,2