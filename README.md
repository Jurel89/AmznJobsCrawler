# Amazon Jobs Scraping Tool

> *In God we trust, all others must bring data*

Personal project aimed at crawling Amazon Jobs portal and modelling some KPIs.

This is probably against the portal policy, but it will only be used for personal/learning purposes. If anyone wants to re-use it, do it at your own risk.

---

## Website behaviour

After doing a few tests with the website, monitoring requests, responses and performance, it seems this site doesn't really have an aggresive anti-bot as retail site does. The API request doesn't ask for any cookie or token, hence we won't have to pass those to a session object.

Since we are only interested in the search results, retrieving the information would only require API calling and json parsing. The only thing to have in mind is the 100 req_id detail limit that can be passed on to the json output.

Even though you can directly query the API throwing a get request to the main API endpoint, you will only get certain aggregated information if you pass some "facets" parameters in that get request. See the differences between the files fullApiGetResponse and plainGetResponse for further details.

## Project Scope

The aim of this project can be defined in two approaches:

1) Extracting aggregated figures for the whole company, worldwide and considering all orgs.
2) Extracting detailed information for each corporate req_id in the EU5 + Lux locales

Besides the general goals, it can be summarized in the tasks below:

- Automating the retrieval of the Amazon Jobs portal information
- Storing the results in a datalake and loading them in a relational db.
- Monitoring the evolution of open reqs
- Build several KPIs, tables and charts
- Automate the reporting with a daily email passing some html

## Geographical Scope

In this first version of the project, we only aim at crawling detailed information at req_id level for the EU5 locales + Lux. However, the code can be used for any other local or for the whole Amazon Jobs portal worldwide.

In any case, we shall monitor the aggregated information for each country/organization, as some orgs might be impacted differently by these layoffs and hiring freezes, but we won't be retrieving that info a req_id level, only aggregated.

## Warnings and Project's limits

There are several cases were we need to be aware of the potential innacurate results or misinformation, before driving conclusions that are not completely certain.

- Whenever certain req_id dissapears, we don't know for sure if it was a cancelled req or an actual hire
- Internal moves might impact those closings as well, we don't have any way of actually identifying the root cause of certain reqs being removed from the site.

## Information Storage

Given that the API directly gives us a json file, we will be storing those original json results persistently, like in a datalake approach. Besides that, and considering the volume of the data won't cause a real performance issue no matter what tecnology we use, we will parse and store all the info in a cheap SQL database, and run analytics on that later on.

## Architecture Design

Since this whole process runs in seconds, we will go for AWS Lambda as the serverless compute service to extract the information, triggered by a time schedule in EventBridge, store it in S3, parse it, and insert that in Amazon RDS MySql Instance. There are better alternatives, but for the sake of time and expenses, this seems like a "good enough" approach.

![alt text](https://github.com/Jurel89/amznJobsScraper/blob/main/localTesting/statics/AmznJobsCrawlerArchitecture.drawio.png?raw=true)

### Considerations

- In the Postgres Insert Lambda folders, the py configuration file that contains the credentials for Amazon RDS has been added to gitignore for obvious security reasons. Make sure you add it to your workspace.
- In the Email Update Lambda folder, the SMTP credentials file has been also added to gitignore for the same reasons, keep that in mind as well