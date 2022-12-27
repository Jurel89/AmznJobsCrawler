import json, sys
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import functions as f, rds_config, smtp_config, smtplib, json, os
import pandas as pd 
sys.path.append('/mnt/access')

def lambda_handler(event, context):
    with open(r'sqlQueries/BusinessCategoryLastWeekEvo.sql','r') as sqlFile:
        BusinessCategorySql = sqlFile.read()
    BusCatRawDF = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, BusinessCategorySql)
    BusCatRawDF['opened_reqs'] = BusCatRawDF['opened_reqs'].astype('int')
    BusCatFinalDF = pd.pivot_table(BusCatRawDF,index='business_category',columns='SNAPSHOT_DATE',values='opened_reqs').reset_index().rename_axis(index=None, columns=None)
    BusCatFinalDF['DoD'] = (BusCatFinalDF.iloc[:, -1] - BusCatFinalDF.iloc[:, -2])/BusCatFinalDF.iloc[:, -2]
    BusCatFinalDF['DoD'] = (BusCatFinalDF['DoD'] * 100).round(2).astype(str) + ' %'
    BusCatFinalDF['WoW'] = (BusCatFinalDF.iloc[:, -2] - BusCatFinalDF.iloc[:, 1])/BusCatFinalDF.iloc[:, 1]
    BusCatFinalDF['WoW'] = (BusCatFinalDF['WoW'] * 100).round(2).astype(str) + ' %'
    BusCatFinalDF = BusCatFinalDF.sort_values(by=BusCatFinalDF.columns[-3],ascending=False)
    BusCatFinalDF = BusCatFinalDF.dropna()
    BusCatHtmlDf = BusCatFinalDF.to_html(index=False)

    #BCountry Dataframe 

    with open(r'sqlQueries/countryCodeLastWeekEvo.sql','r') as sqlFile:
        CountrySql = sqlFile.read()
    CountryRawDF = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, CountrySql)
    CountryRawDF['opened_reqs'] = CountryRawDF['opened_reqs'].astype('int')
    CountryFinalDF = pd.pivot_table(CountryRawDF,index='country_code',columns='SNAPSHOT_DATE',values='opened_reqs').reset_index().rename_axis(index=None, columns=None)
    CountryFinalDF['DoD'] = (CountryFinalDF.iloc[:, -1] - CountryFinalDF.iloc[:, -2])/CountryFinalDF.iloc[:, -2]
    CountryFinalDF['DoD'] = (CountryFinalDF['DoD'] * 100).round(2).astype(str) + ' %'
    CountryFinalDF['WoW'] = (CountryFinalDF.iloc[:, -2] - CountryFinalDF.iloc[:, 1])/CountryFinalDF.iloc[:, 1]
    CountryFinalDF['WoW'] = (CountryFinalDF['WoW'] * 100).round(2).astype(str) + ' %'
    CountryFinalDF = CountryFinalDF.sort_values(by=CountryFinalDF.columns[-3],ascending=False)
    CountryFinalDF = CountryFinalDF.dropna()
    CountryHtmlDf = CountryFinalDF.to_html(index=False)


    # EmpType Dataframe
    with open(r'sqlQueries/EmployeeTypeLastWeekEvo.sql','r') as sqlFile:
        EmpTypeLW_sql = sqlFile.read()
    EmpTypeRawDF = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, EmpTypeLW_sql)
    EmpTypeRawDF['opened_reqs'] = EmpTypeRawDF['opened_reqs'].astype('int')
    EmpTypeFinalDF = pd.pivot_table(EmpTypeRawDF,index='emp_type',columns='SNAPSHOT_DATE',values='opened_reqs').reset_index().rename_axis(index=None, columns=None)
    EmpTypeFinalDF['DoD'] = (EmpTypeFinalDF.iloc[:, -1] - EmpTypeFinalDF.iloc[:, -2])/EmpTypeFinalDF.iloc[:, -2]
    EmpTypeFinalDF['DoD'] = (EmpTypeFinalDF['DoD'] * 100).round(2).astype(str) + ' %'
    EmpTypeFinalDF['WoW'] = (EmpTypeFinalDF.iloc[:, -2] - EmpTypeFinalDF.iloc[:, 1])/EmpTypeFinalDF.iloc[:, 1]
    EmpTypeFinalDF['WoW'] = (EmpTypeFinalDF['WoW'] * 100).round(2).astype(str) + ' %'
    EmpTypeHtmlDf = EmpTypeFinalDF.to_html(index=False)

    # Expertise Area
    with open(r'sqlQueries/exertiseAreaLastWeekEvo.sql','r') as sqlFile:
        ExpAreaLW_sql = sqlFile.read()
    ExpAreaRawDF = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, ExpAreaLW_sql)
    ExpAreaRawDF['opened_reqs'] = ExpAreaRawDF['opened_reqs'].astype('int')
    ExpAreaFinalDF = pd.pivot_table(ExpAreaRawDF,index='expertise_area',columns='SNAPSHOT_DATE',values='opened_reqs').reset_index().rename_axis(index=None, columns=None)
    ExpAreaFinalDF['DoD'] = (ExpAreaFinalDF.iloc[:, -1] - ExpAreaFinalDF.iloc[:, -2])/ExpAreaFinalDF.iloc[:, -2]
    ExpAreaFinalDF['DoD'] = (ExpAreaFinalDF['DoD'] * 100).round(2).astype(str) + ' %'
    ExpAreaFinalDF['WoW'] = (ExpAreaFinalDF.iloc[:, -2] - ExpAreaFinalDF.iloc[:, 1])/ExpAreaFinalDF.iloc[:, 1]
    ExpAreaFinalDF['WoW'] = (ExpAreaFinalDF['WoW'] * 100).round(2).astype(str) + ' %'
    ExpAreaFinalDF = ExpAreaFinalDF.sort_values(by=ExpAreaFinalDF.columns[-3],ascending=False)
    ExpAreaFinalDF = ExpAreaFinalDF.dropna()
    ExpAreaHtmlDf = ExpAreaFinalDF.to_html(index=False)

    # EU5 + Lux Key Recruiting Metrics
    with open(r'sqlQueries/Eu5DailyVariation.sql','r') as sqlFile:
        ExpAreaLW_sql = sqlFile.read()
    KeyMetricsRawDf = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, ExpAreaLW_sql)
    KeyMetricsRawDf['opened_reqs'] = KeyMetricsRawDf['opened_reqs'].astype('int')
    KeyMetricsRawDf['closed_reqs'] = KeyMetricsRawDf['closed_reqs'].astype('int')
    KeyMetricsRawDf['created_reqs'] = KeyMetricsRawDf['created_reqs'].astype('int')
    KeyMetricsRawDf['net_variation'] = KeyMetricsRawDf['net_variation'].astype('int')
    KeyMetricsRawDf['avg_opened_days'] = KeyMetricsRawDf['avg_opened_days'].astype('float')
    KeyMetricsRawDf['avg_closing_days'] = KeyMetricsRawDf['avg_closing_days'].astype('float')
    KeyMetricsFinalDF = KeyMetricsRawDf.sort_values(by=KeyMetricsRawDf.columns[0],ascending=True)
    KeyMetricsFinalDF = KeyMetricsFinalDF.dropna()
    KeyMetricsFinalDF['avg_opened_days'] = KeyMetricsFinalDF['avg_opened_days'].round(decimals = 2)
    KeyMetricsFinalDF['avg_closing_days'] = KeyMetricsFinalDF['avg_closing_days'].round(decimals = 2)
    KeyMetricsHtmlDF = KeyMetricsFinalDF.to_html(index=False)

    # Most Recently Opened Reqs
    with open(r'sqlQueries/EuTop20MostRecentReqsOpened.sql','r') as sqlFile:
        EuMostRecentOpenedReqsSql = sqlFile.read()
    EuMostRecentOpenedReqsRawDf = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, EuMostRecentOpenedReqsSql)
    EuMostRecentOpenedReqsHtmlDf = EuMostRecentOpenedReqsRawDf.to_html(index=False)

    # BI Opened Reqs EU Details
    with open(r'sqlQueries/BiEuOpenedReqsDetails.sql','r') as sqlFile:
        BiOpenedReqsDetailsSql = sqlFile.read()
    BiOpenedReqsDetailsRawDf = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, BiOpenedReqsDetailsSql)
    BiOpenedReqsDetailsHtmlDf = BiOpenedReqsDetailsRawDf.to_html(index=False)

    # EmpType Line Graph
    with open(r'sqlQueries/EmployeeTypeT20DEvo.sql','r') as sqlFile:
        sqlStatement = sqlFile.read()
    empTypeDataframe = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, sqlStatement)
    empTypeDataframe['opened_reqs'] = empTypeDataframe['opened_reqs'].astype('int')
    empTypeFinalDf = empTypeDataframe.pivot(index='SNAPSHOT_DATE', columns='emp_type', values='opened_reqs')
    axes = plt.gca()
    empTypeFinalDf.plot(kind='line', y='TOTAL', ax=axes)
    empTypeFinalDf.plot(kind='line', y='PEOPLE MANAGER', ax=axes)
    empTypeFinalDf.plot(kind='line', y='INDIVIDUAL CONTRIBUTOR', ax=axes)
    plt.xticks(rotation=45, ha="right")
    plt.savefig(r'/tmp/empTypePlot.png')
    plt.close()

    # Eu5+Lux CountryCode Line Graph
    with open(r'sqlQueries/countryCodeT20DEvo.sql','r') as sqlFile:
        sqlStatement = sqlFile.read()
    contryCodeDataframe = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, sqlStatement)
    contryCodeDataframe['opened_reqs'] = contryCodeDataframe['opened_reqs'].astype('int')
    countryCodeFinalDf = contryCodeDataframe.pivot(index='snapshot_date', columns='country_code', values='opened_reqs')
    newAxes = plt.gca()
    countryCodeFinalDf.plot(kind='line', y='ESP', ax=newAxes)
    countryCodeFinalDf.plot(kind='line', y='ITA', ax=newAxes)
    countryCodeFinalDf.plot(kind='line', y='DEU', ax=newAxes)
    countryCodeFinalDf.plot(kind='line', y='LUX', ax=newAxes)
    countryCodeFinalDf.plot(kind='line', y='GBR', ax=newAxes)
    plt.xticks(rotation=45, ha="right")
    plt.savefig(r'/tmp/eu5ContryPlot.png')
    plt.close()

    # WW Main Orgs Line Graph
    with open(r'sqlQueries/mainOrgsT20DEvo.sql','r') as sqlFile:
        sqlStatement = sqlFile.read()
    mainOrgsDataframe = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, sqlStatement)
    mainOrgsDataframe['opened_reqs'] = mainOrgsDataframe['opened_reqs'].astype('int')
    mainOrgsFinalDf = mainOrgsDataframe.pivot(index='snapshot_date', columns='business_category', values='opened_reqs')
    newAxes = plt.gca()
    mainOrgsFinalDf.plot(kind='line', y='Aws', ax=newAxes)
    mainOrgsFinalDf.plot(kind='line', y='Retail', ax=newAxes)
    mainOrgsFinalDf.plot(kind='line', y='Fulfillment & Ops', ax=newAxes)
    plt.xticks(rotation=45, ha="right")
    plt.savefig(r'/tmp/MainOrgsWWPlot.png')
    plt.close()

    # EU5+Lux Target Expertise Are Line Graph
    with open(r'sqlQueries/eu5ExpertiseAreaT20DEvo.sql','r') as sqlFile:
        sqlStatement = sqlFile.read()
    TargetExpertiseAreaRawDf = f.sqlExtractToDataframe(rds_config.db_host, rds_config.db_username, rds_config.db_password, rds_config.db_name, sqlStatement)
    TargetExpertiseAreaRawDf['opened_reqs'] = TargetExpertiseAreaRawDf['opened_reqs'].astype('int')
    TargetExpertiseAreaFinalDf = TargetExpertiseAreaRawDf.pivot(index='snapshot_date', columns='job_category', values='opened_reqs')
    newAxes = plt.gca()
    TargetExpertiseAreaFinalDf.plot(kind='line', y='BIE', ax=newAxes)
    TargetExpertiseAreaFinalDf.plot(kind='line', y='PM-Tech', ax=newAxes)
    TargetExpertiseAreaFinalDf.plot(kind='line', y='PM-NonTech', ax=newAxes)
    TargetExpertiseAreaFinalDf.plot(kind='line', y='Finance', ax=newAxes)
    TargetExpertiseAreaFinalDf.plot(kind='line', y='ISM', ax=newAxes)
    plt.xticks(rotation=45, ha="right")
    plt.savefig(r'/tmp/TargetExpertiseAreaPlot.png')
    plt.close()

    # Creates the final html email passing all html DFs and the style CSS file
    index = open("tmp/emailTemplate.html").read().format(WWOPENEDREQSBYBUSINESS=BusCatHtmlDf,
    WWOPENEDREQSBYEMPTYPE= EmpTypeHtmlDf,
    STYLEFILE= open(r'tmp/style.css').read(),
    WWOPENEDREQSBYCOUNTRY=CountryHtmlDf,
    WWOPENEDREQSBYEXPAREA=ExpAreaHtmlDf,
    EU5TOP20MOSTRECENTOPENEDREQS=EuMostRecentOpenedReqsHtmlDf,
    EU5BIEOPENEDREQS=BiOpenedReqsDetailsHtmlDf,
    WWOPENEDREQEMPTYPEPLOT='/tmp/empTypePlot.png',
    EU5COUNTRYCODETREND='/tmp/eu5ContryPlot.png',
    MAINORGSWWPLOT='/tmp/MainOrgsWWPlot.png',
    TARGETEXPERTISEAREAPLOT='/tmp/TargetExpertiseAreaPlot.png',
    EU5KEYRECRUITINGMETRICS=KeyMetricsHtmlDF)
    with open('/tmp/finalEmail.html','w') as file:
        file.write(index)

    # Sends Email
    strFrom = smtp_config.user
    strTo = smtp_config.toAddress
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Amazon Jobs Daily Update ' + f.todayFileString()
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    with open(r'/tmp/finalEmail.html','r') as file:
        htmlString = file.read()
    msgAlternative.attach(MIMEText(htmlString, 'html'))
    fp = open('/tmp/empTypePlot.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    fp = open('/tmp/eu5ContryPlot.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image2>')
    msgRoot.attach(msgImage)

    fp = open('/tmp/MainOrgsWWPlot.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image3>')
    msgRoot.attach(msgImage)

    fp = open('/tmp/TargetExpertiseAreaPlot.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image4>')
    msgRoot.attach(msgImage)

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(smtp_config.user, smtp_config.appPss)
    text = msgRoot.as_string()
    session.sendmail(strFrom, strTo, text)
    session.quit()
    print('Mail Sent')

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed successfully. Daily Email sent')
    }