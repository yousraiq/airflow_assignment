from urllib import request
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator 

# Define the DAG
dag = DAG(
    dag_id="capstone",
    start_date=days_ago(1),
    schedule_interval="@hourly",
)

# Task 1: Download the data
def _get_data(year, month, day, hour, output_path, **_):
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/"
        f"pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    request.urlretrieve(url, output_path)

get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        "year": "{{ execution_date.year }}",
        "month": "{{ execution_date.month }}",
        "day": "{{ execution_date.day }}",
        "hour": "{{ execution_date.hour }}",
        "output_path": "/tmp/wikipageviews.gz",
    },
    dag=dag,
)

# Task 2: Extract the downloaded gzip file
extract_gz = BashOperator(
    task_id="extract_gz",
    bash_command="gunzip --force /tmp/wikipageviews.gz",
    dag=dag,
)

# Task 3: Fetch the pageviews for specific companies
def _fetch_pageviews(pagenames, execution_date, **_):
    result = dict.fromkeys(pagenames, 0)

    try:
        with open("/tmp/wikipageviews", "r") as f:
            for line in f:
                parts = line.split(" ")
                if len(parts) < 3:
                    continue  # skip malformed lines
                domain_code, page_title, view_counts = parts[:3]
                if domain_code == "en" and page_title in pagenames:
                    result[page_title] += int(view_counts)

        # Write results to SQL file
        with open("/tmp/postgres_query.sql", "w") as f:
            for pagename, pageviewcount in result.items():
                f.write(
                    f"INSERT INTO pageview_counts (pagename, viewcount, execution_date) "
                    f"VALUES ('{pagename}', {pageviewcount}, '{execution_date}');\n"
                )

    except FileNotFoundError:
        print("File not found. Make sure the extraction was successful.")
    
    return result

fetch_pageviews = PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={
        "pagenames": ["Google", "Amazon", "Apple", "Microsoft", "Facebook"]
    },
    dag=dag,
)

# Task 4: Write the results to PostgreSQL
write_to_postgres = PostgresOperator(
    task_id="write_to_postgres",
    postgres_conn_id="my_postgres", 
    sql="/tmp/postgres_query.sql",  # Specify the full path to the SQL file
    dag=dag,
)

# Set task dependencies
get_data >> extract_gz >> fetch_pageviews >> write_to_postgres
