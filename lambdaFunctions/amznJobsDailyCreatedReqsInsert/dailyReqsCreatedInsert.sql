/*
    Why doesn't this guy just use the created_date column to retrieve the daily created reqs?
    Because for some reason there are old reqs that are hidden for some time and then re-appear
    They might be re-using all reqs filled internally, re-activating reqs that were frozen for budget reasons...
    Who knows... In any case, these re-activated reqs are relevant for me, as they indicate an increase in recruitment
*/

INSERT INTO BOOKER.D_DAILY_CREATED_REQ_DETAILS 
	
SELECT 
	t.req_id
	, t.req_description
	, t.company
	, t.job_category
	, t.business_category
	, t.city
	, t.country_code
	, t.location_description
	, t.job_family
	, t.job_function_id
	, t.created_date
	, t.update_since
	, t.snapshot_date
FROM 
		(
		SELECT 
			ddrd.*
		FROM 
			BOOKER.D_DAILY_REQ_DETAILS ddrd 
		WHERE 
			ddrd.snapshot_date in (SELECT DATE('{RUNDATE_YYYYMMDD:}') FROM BOOKER.D_DAILY_REQ_DETAILS)
	
		) t
	LEFT JOIN 
			(
				SELECT 
					ddrd.*
				FROM 
					BOOKER.D_DAILY_REQ_DETAILS ddrd
				WHERE 
					ddrd.snapshot_date in (SELECT DATE('{RUNDATE_YYYYMMDD:}') - INTERVAL 1 DAY FROM BOOKER.D_DAILY_REQ_DETAILS)
			) y
		ON t.req_id = y.req_id 
WHERE 
	y.req_id is null;