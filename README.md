<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#about-gdelt">About GDELT</a></li>
        <li><a href="#project-architecture">Project Architecture</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#configuring-aws-services">Configuring AWS Services</a></li>
        <li><a href="#using-the-code">Using the Code</a></li>
        <li><a href="#putting-it-together">Putting it Together</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project is an ETL pipeline for the GDELT 2.0 Events Database, a dataset compiling events from worldwide news sources with an interesting variety of extracted fields. The general purpose is to prepare and load this data for meaningful human analysis.

My specific objectives in this project:

* To gain experience with AWS Glue, a fully managed cloud ETL service.
* To model data in a real world context.
* To architect and orchestrate a big data ingestion using services common in the industry.
* To improve skill with AWS relational solutions such as RDS & Redshift.
* To understand the benefits of data lakes vs databases vs data warehouses in practice.

<p align="right">(<a href="#top">back to top</a>)</p>

### About GDELT

From their website: <i>"The GDELT Project is the largest, most comprehensive, and highest resolution open database of human society ever created. Just the 2015 data alone records nearly three quarters of a trillion emotional snapshots and more than 1.5 billion location references, while its total archives span more than 215 years, making it one of the largest open-access spatio-temporal datasets in existance and pushing the boundaries of "big data" study of global human society.

The GDELT Project is an initiative to construct a catalog of human societal-scale behavior and beliefs across all countries of the world, connecting every person, organization, location, count, theme, news source, and event across the planet into a single massive network that captures what's happening around the world, what its context is and who's involved, and how the world is feeling about it, every single day."</i>

GDELT data is well documented. The following pages are specifically relevant:
* [Project Homepage](https://www.gdeltproject.org/)
* [More info on the GDELT 2.0 Events Database used in this project](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)
* [Documentation covering the entire project](https://www.gdeltproject.org/data.html#documentation/)
* [Latest GDELT 2.0 Events file](http://data.gdeltproject.org/gdeltv2/lastupdate.txt)

<p align="right">(<a href="#top">back to top</a>)</p>

### Project Architecture

![Architecture Diagram Image][architecture-diagram]

* #1: Lambda uploads the latest GDELT 2.0 Events file to S3.
* #2: Glue cleanses the data sitting in S3.
* #3: Glue enriches the data by joining it with dimension tables in RDS.
* #4: Glue loads the data to the Redshift warehouse.
* #5: From there, integration with Quicksight can provide reports and visual analysis.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Steps to recreate this project are listed below.

### Configuring AWS Services

* You need to configure your VPC, so that Glue can access the datastores. Make sure your security group has a self-referencing inbound rule for all TCP ports (see [here](https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html)). You will likely also need to create a NAT Gateway (make sure it is in the route table) and S3 Gateway (info [here](https://docs.aws.amazon.com/glue/latest/dg/connection-S3-VPC.html)).
* Create an RDS database within the configured VPC. I used MySQL for the engine, but you can choose your preference.
* Create a Redshift cluster within the configured VPC.
* Create an S3 bucket for raw GDELT data with folder "gdelt". Upload the sample file for initial testing (in src/assets/data/) into the foler. Your bucket should be in the same region that you will be using for Glue.
* Create Glue connections for all of the above (RDS, Redshift, S3). Use type "Network" for S3 and type "JDBC" for RDS & Redshift. Use the legacy connections page to test whether your connections are working. This will save you a lot of time when debugging the crawlers and jobs. If your connections fail, it is almost certainly an issue with the VPC configuration.
* Create Glue databases for each of the above. To match the code, names are "gdelt-raw" for S3, "gdelt-reporting" for Redshift, and "gdelt-dimensions" for RDS.
* Create Glue crawlers for each data source. Use the connection and Glue database corresponding to the data source.

### Adding the Code

* Create a new Lambda function and copy the code. Change the bucket name within the script to reflect yours. Make sure Lambda has an execution role with S3 access.
* Use any SQL client to run DDL statements for RDS. You can load the dimension data from .txt files (in src/assets/data/dimensions/) with your client or upload to S3 for import using Glue.
* Redshift DDL statements can be run within the console or via client.
* Create a new Glue job and copy the code. Make sure backtrack is enabled if you plan to load data incrementally.

### Putting it Together

* Run your Glue crawlers for all three datasources. Check that all tables have been added to your catalog. Glue will automatically detect schemas for all tables (including the empty Redshift table).
* Finally, run your Glue job. Check that the Redshift table is populated.
* From here, you could advance the project with orchestration. I would suggest EventBridge to automate Lambda. Glue crawlers/jobs can be scheduled using cron expressions.

Once data is loaded, you can run a variety of interesting queries to analyze the data. For example:
```
SELECT EventCountry AS Country, COUNT(*) AS NumofProtests FROM EventsbyCountryandType
WHERE EventType='PROTEST'
GROUP BY EventCountry
ORDER BY COUNT(*) DESC;
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [DynamicFrame Class](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
* [Setting up network access to datastores](https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html)
* [Conflict and Mediation Event Observations](https://en.wikipedia.org/wiki/Conflict_and_Mediation_Event_Observations)
* [FIPS 10-4](https://en.wikipedia.org/wiki/FIPS_10-4)
* [In Search of Happiness: A Quick ETL Use Case with AWS Glue and Redshift](https://gorillalogic.com/blog/a-quick-etl-use-case-with-aws-glue-redshift/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN IMAGES -->
[architecture-diagram]: /src/assets/images/architecture.jpg
