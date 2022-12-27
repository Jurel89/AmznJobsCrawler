CREATE TABLE IF NOT EXISTS BOOKER.D_DAILY_REQ_DETAILS

(
    req_id VARCHAR(255) NOT NULL -- id_icims
,   req_description VARCHAR(255) -- title
,   company VARCHAR(255) -- company_name
,   job_category VARCHAR(255) -- job_category
,   business_category VARCHAR(255) -- business_category
,   city VARCHAR(255) -- city
,   country_code VARCHAR(255) -- country_code
,   location_description VARCHAR(255) -- location
,   job_family VARCHAR(255) -- job_family
,   job_function_id VARCHAR(255) -- job_function_id
,   created_date DATE -- posted_date
,   update_since VARCHAR(255) -- updated_time
,   snapshot_date DATE NOT NULL -- rundate from python lambda
,   CONSTRAINT req_details_pk PRIMARY KEY (req_id, country_code, snapshot_date) 
);

/* Adding country code as part of the primary key as we dont know if the same req may be published in different countries,
hence retrieved in the different API get requests per country
*/


CREATE TABLE IF NOT EXISTS BOOKER.D_DAILY_GLOBAL_FACETS

(
    SNAPSHOT_DATE DATE NOT NULL -- rundate from python lambda
,   MAIN_FACET_CATEGORY VARCHAR(255) NOT NULL -- top json categories
,   FACET_SUBCATEGORY VARCHAR(255) NOT NULL -- individual json divisions
,   REQ_VALUE INT -- json value, number of opened positions
);