import rds_config, functions as f
bucketName = "amznjobsmainfacets"
targetTable = "BOOKER.D_DAILY_GLOBAL_FACETS"
columnsList = ['SNAPSHOT_DATE','MAIN_FACET_CATEGORY','FACET_SUBCATEGORY','REQ_VALUE']

def lambda_handler(event, context):
    jsonFileName = 'globalMainFacets_' + f.todayFileString() + ".json"
    f.s3FileDownloader(bucketName, jsonFileName, "/tmp/" + jsonFileName)
    SqlStatement = f.mainFacetsJsonToInsertSql("/tmp/" + jsonFileName, targetTable, columnsList, f.todayFileString())
    f.runSqlStatementMySQL(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, SqlStatement)
