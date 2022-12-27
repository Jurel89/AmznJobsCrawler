import requests, json, math
import datetime, boto3

def todayFileString():
    today = datetime.date.today()
    todays_day = today.day
    todays_day = '{:02d}'.format(todays_day)
    todays_month = today.month
    todays_month = '{:02d}'.format(todays_month)
    todays_year = today.year
    today_date_string = str(todays_year) + str(todays_month) + str(todays_day)
    return today_date_string

def apiParamsContructor(offset, **kwargs):
    params = {
        'schedule_type_id': 'Full Time'
        , 'result_limit': 100
        , 'offset': offset
        , 'job_function_id[]': 'job_function_corporate_80rdb4'
        }
    params.update(**kwargs)
    return params

def apiJobDetailsCrawler(filepath, **kwargs):
    mainApiEndpoint = r'https://www.amazon.jobs/es/search.json?'
    r = requests.get(mainApiEndpoint, params=apiParamsContructor(0,**kwargs))
    parsedJson = json.loads(r.content)
    hits = parsedJson['hits']
    loopNum = math.ceil(hits/100)
    if loopNum > 1:
        for i in range(1,loopNum):
            loopOffset = i * 100
            loopParams = apiParamsContructor(loopOffset,**kwargs)
            loopR = requests.get(mainApiEndpoint, params=loopParams)
            loopJson = json.loads(loopR.content)
            parsedJson["jobs"].append(loopJson["jobs"])
    with open(filepath, 'w') as f:
        json.dump(parsedJson, f, indent=4, sort_keys=True)

def s3FileUploader(bucketName, fileName, lambdaPath):
    lambda_path = lambdaPath + fileName
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(lambda_path, bucketName, fileName)
