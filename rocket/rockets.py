# import airflow
# from airflow import DAG
# from airflow.utils.dates import datetime
# from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator

# from rockets.includes.get_picture import _get_pictures
# from airflow.models import Variables 

# email_sender = "ayesha@mailinator.com"
# email_password = "12345678"

# def task_fail_alert (context):
#     state = context.get("task_instance").state
#     dag = context.get("task_instance").dag_id
#     task = context.get("task_instance").task_id
#     exact_date = context.get("task_instance").state_date
#     log = context.get("task_instance").log_url
#     env_name =context["params"].get("environment")

#     subject = f"task {task} in dag {dag} failed"    
#     body = f'''


#             task {task} in dag {dag} failed


#             '''

# arg = {
#     "on_failure_callback": task_fail_alert,
#     "params": {
#         "environment": Variables.get("environment")
#     }
# }
# # dag = DAG(
# #     dag_id="rocket",
# #     start_date=datetime(2024, 10, 2),
# #     schedule_interval=None
# # )

# #Instantiate a DAG object; this is the starting point of any workflow
# with DAG(
#     dag_id="rocket",  #The name of the DAG
#     start_date=datetime(2024, 10, 4), #The date at which the DAG should first start running
#     schedule_interval=None,  #At what interval the DAG should run
#     catchup=False,
#     default_args = arg

#     #tag="CoreDataEngineers"
# ) as dag:
    
#     #Apply Bash to download the URL response with curl
#     download_launches = BashOperator(
#         task_id="download_launches",
#         bash_command="curl -o /opt/airflow/dags/rockets/launches/launches.json -L https://ll.thespacedevs.com/2.0.0/launch/upcoming"
#     )


    
#     #Call the Python function in the DAG with a PythonOperator
#     get_pictures = PythonOperator(
#         task_id="get_pictures", 
#         python_callable=_get_pictures
#     )

#     notify = BashOperator(
#         task_id="notify",
#         bash_command='echo "There are now $(ls /opt/airflow/dags/rockets/images/ | wc -1) image"'
#     )

#     #Set the order of execution of tasks.
#     download_launches >> get_pictures >> notify