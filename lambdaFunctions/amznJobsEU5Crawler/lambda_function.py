import functions as f
countryCrawlingList = ['ESP','ITA','FRA','DEU','GBR','LUX']

def lambda_handler(event, context):
    for i in countryCrawlingList:
        f.apiJobDetailsCrawler("/tmp/" + i + '_JobFullDetails_' + f.todayFileString() + '.json',country=i)
        f.s3FileUploader('amznjobseu5fulldetails', i + '_JobFullDetails_' + f.todayFileString() + '.json', "/tmp/")


