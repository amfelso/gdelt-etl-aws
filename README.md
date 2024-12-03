<!-- PROJECT TITLE -->
# Cloud ETL Pipeline for GDELT Data

Efficiently process and analyze large-scale global events data using a serverless cloud ETL pipeline built with AWS Glue, Lambda, S3, RDS, and Redshift.

<!-- BADGES -->
[![AWS Certified Solutions Architect](https://img.shields.io/badge/AWS-Solutions%20Architect%20Professional-blue)](https://www.credly.com)
[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#objectives">Objectives</a></li>
        <li><a href="#architecture-overview">Architecture Overview</a></li>
      </ul>
    </li>
    <li><a href="#skills-showcased">Skills Showcased</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#queries-and-visualizations">Queries and Visualizations</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

---

## About the Project

This project demonstrates my ability to design, implement, and orchestrate a cloud-based ETL pipeline. It uses the [GDELT 2.0 Events Database](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/) to extract, transform, and load (ETL) data for advanced analytics.

### Objectives
- Gain hands-on experience with **AWS Glue** and serverless ETL workflows.
- Design a **scalable architecture** for real-world big data processing.
- Integrate **RDS and Redshift** to support robust analytics and reporting.
- Explore **data lakes vs. data warehouses** in practical use cases.

---

## Architecture Overview

![Architecture Diagram](https://github.com/amfelso/gdelt-etl-aws/blob/b6f06b4363502b11e688724e4e44daa25de2a8f4/src/assets/images/architecture.jpg)

**Pipeline Flow**:
1. **Data Ingestion**: A Lambda function downloads the latest GDELT data and uploads it to S3.
2. **Data Transformation**: AWS Glue cleanses and enriches the raw data.
3. **Data Loading**: The enriched data is loaded into Redshift for querying and visualization.
4. **Reporting**: Tools like Amazon QuickSight can be used for visualization.

---

## Skills Showcased

- **Cloud Architecture**: Designed and implemented a serverless pipeline using AWS services.
- **Big Data Processing**: Transformed and loaded global-scale data using AWS Glue and Redshift.
- **Data Modeling**: Integrated normalized dimension tables in RDS for better query performance.
- **Automation**: Recommended the use of EventBridge for orchestration.
- **SQL Expertise**: Ran advanced queries for actionable insights from GDELT data.

---

## Getting Started

### Prerequisites
1. **AWS Account**: Ensure your AWS environment is set up with IAM roles for Glue, Lambda, and S3.
2. **Services**: Configure VPCs, RDS, Redshift, and S3 buckets for data storage.

### Steps
1. **Setup AWS Services**:
   - Configure Glue connections for RDS, Redshift, and S3.
   - Set up Lambda with the provided script.
   - Create Glue crawlers for raw data ingestion and schema detection.

2. **Run the ETL Pipeline**:
   - Execute Lambda to ingest GDELT data into S3.
   - Use Glue jobs to transform and enrich data.
   - Load final datasets into Redshift for querying.

---

## Queries and Visualizations

Here are some sample queries to demonstrate the pipeline's output:

### Top 5 Countries by Protest Count
```sql
SELECT EventCountry AS Country, COUNT(*) AS NumOfProtests
FROM EventsByCountryAndType
WHERE EventType='PROTEST'
GROUP BY EventCountry
ORDER BY COUNT(*) DESC
LIMIT 5;
