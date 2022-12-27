SELECT
	ddgf.FACET_SUBCATEGORY as expertise_area
	, ddgf.SNAPSHOT_DATE 
	, ddgf.REQ_VALUE as opened_reqs
FROM 
	BOOKER.D_DAILY_GLOBAL_FACETS ddgf 
WHERE 
	ddgf.SNAPSHOT_DATE between DATE(NOW() - INTERVAL 8 DAY) AND DATE(NOW()) AND 
	ddgf.MAIN_FACET_CATEGORY = 'category_facet'