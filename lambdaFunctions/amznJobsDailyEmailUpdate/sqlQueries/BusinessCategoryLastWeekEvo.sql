SELECT
	CASE 
		WHEN ddgf.FACET_SUBCATEGORY = 'aws' THEN 'Aws'
		WHEN ddgf.FACET_SUBCATEGORY in ('retail','amazon-business', 'amazongo','amazonfresh','amazon-books',
										'pharmacy','healthcare') THEN 'Retail'
		WHEN ddgf.FACET_SUBCATEGORY in ('fulfillment-and-operations','operations','fulfillment-ops','transportation-and-logistics'
										,'fulfillment-ops-team','operations-team') THEN 'Fulfillment & Ops'
		WHEN ddgf.FACET_SUBCATEGORY in ('amazon-customer-service','customer-service') THEN 'Customer Service'
		WHEN ddgf.FACET_SUBCATEGORY in ('amazondevices','alexa','amazon-devices','devices') THEN 'Amazon Devices'
		WHEN ddgf.FACET_SUBCATEGORY in ('studentprograms','university') THEN 'Student Programs'
		WHEN ddgf.FACET_SUBCATEGORY in ('humanresources','hr','recruitingengine') THEN 'Human Resources'
		WHEN ddgf.FACET_SUBCATEGORY in ('seller-services', 'marketplace') THEN 'Marketplace & Seller Services'
		ELSE ddgf.FACET_SUBCATEGORY END as business_category
	, ddgf.SNAPSHOT_DATE 
	, sum(ddgf.REQ_VALUE) as opened_reqs
FROM 
	BOOKER.D_DAILY_GLOBAL_FACETS ddgf 
WHERE 
	ddgf.SNAPSHOT_DATE between DATE(NOW() - INTERVAL 8 DAY) AND DATE(NOW()) AND 
	ddgf.MAIN_FACET_CATEGORY = 'business_category_facet'
GROUP BY 1, 2
