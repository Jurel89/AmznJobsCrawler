import functions as f, rds_config, json

def lambda_handler(event, context):
    with open(r'dailyReqsCreatedInsert.sql','r') as file:
        rawSql = file.read().format(RUNDATE_YYYYMMDD=f.todayFileString())
    f.runSqlStatementMySQL(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, rawSql)
    return {
        'statusCode': 200,
        'body': json.dumps('Daily Created Reqs Insert executed successfully')
    }