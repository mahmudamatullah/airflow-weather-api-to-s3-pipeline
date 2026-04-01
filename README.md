# Weather API to S3 Data Pipeline
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-%235835CC.svg?style=flat&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10.4-blue.svg?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-%23017CEE.svg?style=flat&logo=apache-airflow&logoColor=white)

## Table of Contents

- [Project Overview](#project-overview)
- [Infrastructure / Architecture](#infrastructure--architecture)
- [Data Generation](#data-generation)
- [Data Pipeline Flow](#data-pipeline-flow)
- [Tech Stack](#tech-stack)
- [How to Run](#how-to-run)
- [Key Features](#key-features)
- [Future Improvements](#future-improvements)
- [What I Learnt](#what-i-learnt)
- [Next Projects](#next-projects)

---

## Overview

This project is an automated data ingestion pipeline that fetches real-time weather data from an external API and stores it in Amazon S3 in Parquet format.

It is a fully orchestrated using Apache Airflow, with Terraform provisioned infrastructure and sensitive credentials securely managed using AWS Systems Manager (SSM) Parameter Store.

> No scripts are run manually Airflow handles scheduling, execution, and retries.
--- 

## Infrastructure / Architecture
Infrastructure is provisioned using Terraform and includes:
- Amazon S3 bucket for data storage
- IAM user with restricted S3 permissions
- IAM access keys generated programmatically
- AWS SSM Parameter Store for secure credential storage

## Data Generation
Data is fetched from the Weatherbit API
- Location used: Lagos, Nigeria (latitude & longitude based)
- API returns real-time weather data


## Data Pipeline Flow
1. Terraform provisions AWS resources (S3, IAM, SSM).
2. Airflow DAG (weather_api_to_s3) runs daily.
3. PythonOperator triggers extract_weather_data()
- The function:
  - Retrieves API key and AWS credentials from Airflow Variables
  - Calls the Weather API
  - Transforms JSON response into a Pandas DataFrame
  - Writes data to S3 in Parquet format
4. Files are stored in S3 with a date-based naming convention

> Key point: The python script is not triggered manually. Airflow orchestrates the execution, making the workflow automated and scheduled.

## Tech Stack
- Python (requests, pandas, awswrangler)
- Apache Airflow (orchestration & scheduling)
- AWS S3 (data storage)
- Terraform (infrastructure as code)
- AWS IAM (access control)
- AWS SSM Parameter Store (secure credential management)
- Docker (Airflow local setup)

## How to Run

### 1. Prerequisites
Before running the pipeline, you need to have:

- An AWS account with access
- Terraform installed locally
- Docker installed
- Apache Airflow installed via Docker, or the script can be copied if it's on the cloud.
- Optional: Python (for local scripts/tests)

---

### 2. Provision AWS Infrastructure
``bash
terraform init
terraform apply``

> Terraform will create the necessary resources mentioned in the Architecture/ Infrastructure
> Note: Replace any placeholder variables in Terraform with your own AWS credentials and preferred naming.
> Ensure variables for RDS credentials (db_name, db_username, db_password) are set.

### 3. Start Airflow (Docker)
`docker-compose up` - This will launch the Airflow webserver and scheduler locally.

Access the Airflow UI at:
`http://localhost:8080`

4. Configure Airflow Variables

| Variable Name   | Description     |
| --------------- | --------------- |
| ACCESS_KEY      | AWS access key  |
| SECRET_KEY      | AWS secret key  |
| weather_api_key | Weather API key |

You can use placeholder values to test or your own credentials.

- Open Airflow UI, locate weather_api_to_s3 and trigger it.
- Airflow will:
  - Fetch weather data
  - Transform it
  - Store it in S3 automatically

5. Notes
This project is intended to be run with your own AWS account.

## Key Features
- Fully automated pipeline (no manual execution)
- Airflow-based orchestration with retries
- Secure credential handling via Airflow Variables + SSM
- Infrastructure fully managed with Terraform
- Parquet format for efficient storage
- Date-partitioned file naming

## Future Improvements
- Partition data by date in S3 for better querying
- Add data validation checks before upload
- Integrate downstream analytics (e.g., Athena or Redshift)
- Implement monitoring and alerting

## What I Learned
- Building production-style API ingestion pipelines
- Using Airflow for orchestration instead of manual execution
- Managing sensitive credentials securely (SSM + Airflow Variables)
- Writing efficient data to S3 using Parquet format
- Structuring Terraform for IAM and storage resources
