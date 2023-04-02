from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.python import PythonOperator
import psycopg2
import time

def get_log_connection(): # connect to db logs 
    conn_etl_logs = psycopg2.connect(
        database='inovus_logs', 
        host='host.docker.internal', 
        user='inovus', 
        password='postgres',
        port="5434"
    )
    return conn_etl_logs

def get_inovus_connection(): # connect to inovus db
    conn_inovus = psycopg2.connect(
        database="inovus",
        host="host.docker.internal",
        user="inovus",
        password="postgres",
        port="5433"
    )
    return conn_inovus

def create_log_suc(name):
    conn_log = get_log_connection() 
    cur = conn_log.cursor() 
    cur.execute('insert into logs.etl_logs (event_time, event_type, message) VALUES (%s, %s, %s)', (time.asctime(), 'INFO', f'{name} - task finished')) 
    conn_log.commit()
    conn_log.close() 

def create_log_er(name):
    conn_log = get_log_connection() 
    cur = conn_log.cursor() 
    cur.execute('insert into logs.etl_logs (event_time, event_type, message) VALUES (%s, %s, %s)', (time.asctime(), 'ERROR', f'{name} - task failed')) 
    conn_log.commit()
    conn_log.close() 

def etl_inovus_dwh_f_sale(): # etl from mrr.fact_sales to stg.fact_sales
    try:
        conn_inovus = get_inovus_connection() # 1
        cur = conn_inovus.cursor() # 1
        cur.execute("select * from stg.fact_sales;") # 1
        rows = cur.fetchall() # 1
        cur.executemany('insert into dwh.fact_sales values (%s, %s, %s)', rows) # 2
        create_log_suc('etl_inovus_dwh_f_sale')
    except:
        create_log_er('etl_inovus_dwh_f_sale')
        raise Exception
    conn_inovus.commit()
    conn_inovus.close() # 1

def etl_inovus_dwh_dimcustomer(): # etl from mrr.dimension_custimer to stg.dimension_custimer
    try:    
        conn_inovus = get_inovus_connection() # 1
        cur = conn_inovus.cursor() # 1
        cur.execute("select * from stg.dimension_customer;") # 1
        rows = cur.fetchall() # 1
        cur.executemany('insert into dwh.dimension_customer values (%s, %s, %s)', rows) # 2
        create_log_suc('etl_inovus_dwh_dim_customer')
    except:
        create_log_er('etl_inovus_dwh_dim_customer')
        raise Exception
    conn_inovus.commit()
    conn_inovus.close() # 1

def etl_inovus_dwh_dimproducts(): # etl from mrr.dimension_products to stg.dimension_products
    try:
        conn_inovus = get_inovus_connection() # 1
        cur = conn_inovus.cursor() # 1
        cur.execute("select * from stg.dimension_products;") # 1
        rows = cur.fetchall() # 1
        cur.executemany('insert into dwh.dimension_products values (%s, %s, %s)', rows) # 2
        create_log_suc('etl_inovus_dwh_dim_products')
    except:
        create_log_er('etl_inovus_dwh_dim_products')
        raise Exception
    conn_inovus.commit()
    conn_inovus.close() # 1

def update_high_water_mark():
    conn_inovus = get_inovus_connection()
    cur = conn_inovus.cursor()
    cur.execute("update dwh.high_water_mark SET date_update = now() WHERE name_db = 'dwh';")
    conn_inovus.commit()
    conn_inovus.close()
    
with DAG(
    dag_id='inovus_etl_dag_stg_to_dwh',
    schedule_interval='@daily',
    start_date=days_ago(2),
    tags=['etl']
    ) as dag:
    
    task_sales  = PythonOperator(
        task_id = 'etl_from_stgfsales_to_dwhfsales',
        python_callable = etl_inovus_dwh_f_sale
    )

    task_customer = PythonOperator(
        task_id = 'etl_from_stgdimcustomer_to_dwhdimcustomer',
        python_callable = etl_inovus_dwh_dimcustomer
    )

    task_products = PythonOperator(
        task_id = 'etl_from_stgdimcproducts_to_dwhdimcproducts',
        python_callable = etl_inovus_dwh_dimproducts
    )

    task_high_water_mark = PythonOperator(
        task_id = 'date_update_dwh',
        python_callable = update_high_water_mark
    )




task_customer >> task_products >> task_sales >> task_high_water_mark
  