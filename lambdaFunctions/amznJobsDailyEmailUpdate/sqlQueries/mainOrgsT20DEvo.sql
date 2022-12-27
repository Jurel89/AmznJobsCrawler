SELECT
	CASE 
		WHEN ddgf.FACET_SUBCATEGORY = 'aws' THEN 'Aws'
		WHEN ddgf.FACET_SUBCATEGORY in ('retail','amazon-business', 'amazongo','amazonfresh','amazon-books',
										'pharmacy','healthcare') THEN 'Retail'
		WHEN ddgf.FACET_SUBCATEGORY in ('fulfillment-and-operations','operations','fulfillment-ops','transportation-and-logistics'
										,'fulfillment-ops-team','operations-team') THEN 'Fulfillment & Ops'
		END as business_category
	, ddgf.snapshot_date 
	, sum(ddgf.REQ_VALUE) as opened_reqs
FROM 
	BOOKER.D_DAILY_GLOBAL_FACETS ddgf 
WHERE 
	ddgf.SNAPSHOT_DATE between DATE(NOW() - INTERVAL 20 DAY) AND DATE(NOW()) AND 
	ddgf.MAIN_FACET_CATEGORY = 'business_category_facet' AND 
	ddgf.FACET_SUBCATEGORY in ('aws','retail','amazon-business', 'amazongo','amazonfresh','amazon-books',
								'pharmacy','healthcare', 'fulfillment-and-operations','operations','fulfillment-ops',
								'transportation-and-logistics','fulfillment-ops-team','operations-team')
GROUP BY 1, 2
