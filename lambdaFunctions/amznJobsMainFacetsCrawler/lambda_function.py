import json, boto3
import requests
import functions

s3_client = boto3.client('s3')

apiEndpoint = r'https://www.amazon.jobs/es/search.json?&facets%5B%5D=normalized_country_code&facets%5B%5D=normalized_state_name&facets%5B%5D=normalized_city_name&facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&facets%5B%5D=job_function_id&facets%5B%5D=is_manager&facets%5B%5D=is_intern&result_limit=1'

def lambda_handler(event, context):
    r = requests.get(apiEndpoint)
    fullApiData = r.json()
    with open("/tmp/" + "globalMainFacets_" + functions.todayFileString() + ".json", 'w') as f:
        json.dump(fullApiData, f, indent=4, sort_keys=True)
    bucket_name = "amznjobsmainfacets"
    file_name = "globalMainFacets_" + functions.todayFileString() + ".json"
    lambda_path = "/tmp/" + file_name
    s3_path = "amznjobsmainfacets/" + file_name
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(lambda_path, bucket_name, file_name)

    return {
        'statusCode': 200,
        'body': json.dumps('file is created in:'+s3_path)
    }