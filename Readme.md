<h2> Airflow Capstone Project: Wikipedia Pageviews Analysis </h2>

<h3>Overview</h3>
This project is an Airflow DAG designed to download, process, and store Wikipedia pageview data for specific companies. It retrieves hourly pageview data, extracts the relevant information, and writes the results to a PostgreSQL database.

<h3>Table of Contents</h3>
<li>
Prerequisites
Setup
DAG Details
Usage
Tasks
Database Schema
</li>

<h3>Prerequisites</h3>
Python: Version 3.6 or higher
Apache Airflow: Version 2.0 or higher
PostgreSQL: A running instance with the required database and table
Docker: (if using Docker for deployment)

<h3>Setup</h3>
<h4>Clone the Repository:</h4>
git clone https://github.com/USERNAME/my-airflow-project.git
cd my-airflow-project

<h4>Set Up PostgreSQL:<h4>
Ensure that you have a PostgreSQL instance running and create the following table:
CREATE TABLE pageview_counts (
    pagename VARCHAR(255),
    viewcount INTEGER,
    execution_date TIMESTAMP
);

<h4>Configure Airflow:</h4>
Ensure your Airflow environment is set up correctly.
Create a connection in Airflow for PostgreSQL with the conn_id set to my_postgres.

<h3>DAG Details</h3>
The DAG defined in this project is named capstone and runs on an hourly schedule. It consists of four main tasks:

1. Download Wikipedia Pageviews Data:
    Fetches the gzip file containing pageviews data for the current execution date.
    
2. Extract the Downloaded Data:
    Unzips the downloaded gzip file.

3. Fetch Pageviews for Specific Companies:
    Parses the extracted file and counts the pageviews for specified companies: Google, Amazon, Apple, Microsoft, and Facebook.

4. Write Results to PostgreSQL:
    Writes the counted pageviews into a PostgreSQL database

<h3>Usage</h3>
<h4>Start Airflow:</h4>
1. If using Docker, run the following command:
    docker-compose up

2. If using a local Airflow installation, start the Airflow web server and scheduler:
    airflow webserver --port 8080
    airflow scheduler

<h4>Access the Airflow UI:</h4>
Open your web browser and navigate to http://localhost:8080 to view and trigger the DAG.

<h4>Trigger the DAG:</h4>
From the Airflow UI, you can manually trigger the capstone DAG and monitor the execution of each task

<h3>Tasks</h3>
get_data: Downloads the Wikipedia pageviews data.
extract_gz: Unzips the downloaded data file.
fetch_pageviews: Parses the data to count pageviews for specific companies.
write_to_postgres: Inserts the results into the PostgreSQL database.

<h3>Database Schema</h3>
The results are stored in the pageview_counts table with the following schema:
<table>
  <tr>
    <th>Column Name</th>
    <th>Type</th>
  </tr>
  <tr>
    <td>viewcount</td>
    <td>execution_date</td>
  </tr>
  <tr>
    <td>INTEGER</td>
    <td>TIMESTAMP</td>
  </tr>
</table>

