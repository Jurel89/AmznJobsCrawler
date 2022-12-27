import sys, logging, pymysql, datetime
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

def todayFileString():
    today = datetime.date.today()
    todays_day = today.day
    todays_day = '{:02d}'.format(todays_day)
    todays_month = today.month
    todays_month = '{:02d}'.format(todays_month)
    todays_year = today.year
    today_date_string = str(todays_year) + str(todays_month) + str(todays_day)
    return today_date_string