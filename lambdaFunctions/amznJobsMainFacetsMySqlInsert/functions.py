import sys, logging, json, datetime, boto3, pymysql
from dateutil.parser import parse

def todayFileString():
    today = datetime.date.today()
    todays_day = today.day
    todays_day = '{:02d}'.format(todays_day)
    todays_month = today.month
    todays_month = '{:02d}'.format(todays_month)
    todays_year = today.year
    today_date_string = str(todays_year) + str(todays_month) + str(todays_day)
    return today_date_string

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except:
        return False

def runSqlStatementMySQL(rds_host, dbUser, dbPassword, dbName, sqlStatement):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        conn = pymysql.connect(host=rds_host, user=dbUser, passwd=dbPassword, db=dbName, connect_timeout=20)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    with conn.cursor() as cur:
        cur.execute(sqlStatement)
    conn.commit()

def s3FileDownloader(bucketName, fileName, localFileName):
    s3 = boto3.resource("s3")
    s3.meta.client.download_file(bucketName, fileName, localFileName)

def jobDetailsJsonToInsertSql(jsonFilePath, dbTable, jsonKeysList, columnsList):
    myJson = json.load(open(jsonFilePath,'r'))
    insertSqlStatement = []
    for job in myJson["jobs"]:
        insertValues = []
        for field in jsonKeysList:
            value = job[field]
            if type(value) in (str, bytes):
                if is_date(value):
                    value = "'" + str(parse(value).date()) + "'"
                else:
                    value = "'" + value + "'"
            insertValues.append(value)
        snapshotDate = f"'{str(parse(todayFileString()).date())}'"
        insertValues.append(snapshotDate)
        insertValues = ["''" if thing is None else thing for thing in insertValues]
        loopInsert = '(' + ','.join(insertValues) + ')'
        insertSqlStatement.append(loopInsert)
    insertSqlStatement = 'INSERT INTO ' + dbTable + '(' + ','.join(columnsList) + ')' + ' VALUES ' + ','.join(insertSqlStatement)
    return insertSqlStatement

def mainFacetsJsonToInsertSql(jsonFilePath, dbTable, columnsList, snapshotDate):
    insertSqlValues= []
    myJson = json.load(open(jsonFilePath,'r'))
    for facet in myJson['facets']:
        mainCategoryFacet = facet
        snapshotDate = f"'{str(parse(snapshotDate).date())}'"
        for subcategory in myJson['facets'][facet]:
            for key, value in subcategory.items():
                key = key.replace("'", "") if "'" in key else key
                loopInsertValues = "( {} , '{}' , '{}', {} )".format(snapshotDate, mainCategoryFacet, key, value)
                insertSqlValues.append(loopInsertValues)
    insertSqlStatement = 'INSERT INTO ' + dbTable + '(' + ','.join(columnsList) + ')' + ' VALUES ' + ','.join(insertSqlValues)
    return insertSqlStatement

# columnsList = ['SNAPSHOT_DATE','MAIN_FACET_CATEGORY','FACET_SUBCATEGORY','REQ_VALUE']
# testSqlInsert = mainFacetsJsonToInsertSql(r'/Users/joseibanezortiz/Documents/amznJobsScraper/localTesting/statics/fullApiGetRespone.json','BOOKER.D_DAILY_GLOBAL_FACETS', columnsList)
# with open(r'/Users/joseibanezortiz/Documents/amznJobsScraper/localTesting/statics/testInsert.sql','w') as f:
#     f.write(testSqlInsert)