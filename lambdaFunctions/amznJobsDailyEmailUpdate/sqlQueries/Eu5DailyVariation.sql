    SELECT 
	main.snapshot_date
	, main.opened_reqs
	, IFNULL(cl.closed_reqs,0) as closed_reqs
	, IFNULL(cr.created_reqs,0) as created_reqs
    , IFNULL(cr.created_reqs,0) - IFNULL(cl.closed_reqs,0) as net_variation
    , main.avg_opened_days
	, IFNULL(avg_closing_days,0) as avg_closing_days
	
FROM 
	(
		SELECT 
			ddrd.snapshot_date
			, count(DISTINCT ddrd.req_id) as opened_reqs
			, AVG(DATEDIFF(ddrd.snapshot_date, ddrd.created_date)) as avg_opened_days
		FROM 
			BOOKER.D_DAILY_REQ_DETAILS ddrd
		WHERE 
			ddrd.snapshot_date BETWEEN DATE(NOW()) - INTERVAL 13 DAY AND DATE(NOW())
		GROUP BY 1
	) main
	LEFT JOIN 
	(
	SELECT 
		ddcrd.snapshot_date
		, COUNT(DISTINCT ddcrd.req_id) as closed_reqs
		, AVG(DATEDIFF(ddcrd.snapshot_date, ddcrd.created_date)) as avg_closing_days
	FROM 
		BOOKER.D_DAILY_CLOSED_REQ_DETAILS ddcrd 
	GROUP BY 1
	) cl
		ON main.snapshot_date = cl.snapshot_date
	LEFT JOIN 
	(
	SELECT 
		ddcrd.snapshot_date
		, COUNT(DISTINCT ddcrd.req_id) as created_reqs
	FROM 
		BOOKER.D_DAILY_CREATED_REQ_DETAILS ddcrd 
	GROUP BY 1
	) cr 
		ON main.snapshot_date = cr.snapshot_date