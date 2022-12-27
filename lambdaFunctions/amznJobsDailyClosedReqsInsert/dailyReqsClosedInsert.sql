INSERT INTO BOOKER.D_DAILY_CLOSED_REQ_DETAILS  
	
SELECT 
	y.req_id
	, y.req_description
	, y.company
	, y.job_category
	, y.business_category
	, y.city
	, y.country_code
	, y.location_description
	, y.job_family
	, y.job_function_id
	, y.created_date
	, y.update_since
	, DATE(y.snapshot_date + INTERVAL 1 DAY) as snapshot_date

FROM 
		(
		SELECT 
			ddrd.*
		FROM 
			BOOKER.D_DAILY_REQ_DETAILS ddrd 
		WHERE 
			ddrd.snapshot_date in (SELECT DATE('{RUNDATE_YYYYMMDD:}') - INTERVAL 1 DAY FROM BOOKER.D_DAILY_REQ_DETAILS)
	
		) y
	LEFT JOIN  
			(
				SELECT 
					ddrd.*
				FROM 
					BOOKER.D_DAILY_REQ_DETAILS ddrd
				WHERE 
					ddrd.snapshot_date in (SELECT DATE('{RUNDATE_YYYYMMDD:}') FROM BOOKER.D_DAILY_REQ_DETAILS)
			) t
		ON y.req_id = t.req_id 
WHERE 
	t.req_id is null;