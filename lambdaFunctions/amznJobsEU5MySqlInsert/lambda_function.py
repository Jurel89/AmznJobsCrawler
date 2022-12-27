import rds_config, functions as f
countryCrawlingList = ["ESP","ITA","FRA","DEU","GBR","LUX"]
bucketName = "amznjobseu5fulldetails"
finalS3fileList = []
sqlStatementsList = []
targetTable = "BOOKER.D_DAILY_REQ_DETAILS"
jsonKeyList = ["id_icims","title","company_name","job_category","business_category","city","country_code","location","job_family","job_function_id","posted_date","updated_time"]
columnsList = ["req_id","req_description","company","job_category","business_category","city","country_code","location_description","job_family","job_function_id","created_date","update_since","snapshot_date"]


def lambda_handler(event, context):
    for country in countryCrawlingList:
        loopFile = country + "_JobFullDetails_" + f.todayFileString() + ".json"
        f.s3FileDownloader(bucketName, loopFile, "/tmp/" + loopFile)
        finalS3fileList.append("/tmp/" + loopFile)
    for file in finalS3fileList:
        loopSqlStatement = f.jobDetailsJsonToInsertSql(file, targetTable, jsonKeyList, columnsList)
        sqlStatementsList.append(loopSqlStatement)
    for sqlStatement in sqlStatementsList:
        f.runSqlStatementMySQL(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, sqlStatement)
