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

def get_inovus_odb_p_connection(): # connnect to postgress ra-db
    conn_postgres = psycopg2.connect(
        database="inovus_odb",
        host="host.docker.internal",
        user="inovus",
        password="postgres",
        port="5435"
    )
    return conn_postgres

def get_inovus_i_connection(): # connect to inovus db
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
    
def etl_to_mmr_f_sale(): # etl from ra-db.sales to mmr.fact_sales
    try:
        conn_postgres = get_inovus_odb_p_connection() # 1
        cur_p = conn_postgres.cursor() # 1
        cur_p.execute('select * from odb_inovus.sales;') # 1
        rows = cur_p.fetchall() # 1
        conn_inovus = get_inovus_i_connection() # 2
        cur_i = conn_inovus.cursor() # 2
        cur_i.executemany('insert into mrr.fact_sales values (%s, %s, %s)', rows) # 2
        create_log_suc('etl_to_mmr_f_sale')
    except:
        create_log_er('etl_to_mmr_f_sale')
        raise Exception 
    conn_inovus.commit() # 2
    conn_inovus.close() # 2
    conn_postgres.close() # 1

def etl_to_mmr_dim_customer(): # etl from ra-db.customer to mmr.dimension_customer
    try:
        conn_postgres = get_inovus_odb_p_connection() # 1
        cur_p = conn_postgres.cursor() # 1
        cur_p.execute('select * from odb_inovus.customer;') # 1
        rows = cur_p.fetchall() # 1
        conn_inovus = get_inovus_i_connection() # 2
        cur_i = conn_inovus.cursor() # 2
        cur_i.executemany('insert into mrr.dimension_customer values (%s, %s, %s)', rows) # 2
        create_log_suc('etl_to_mmr_dim_customer')
    except:
        create_log_er('etl_to_mmr_dim_customer')
        raise Exception
    conn_inovus.commit() # 2
    conn_inovus.close() # 2
    conn_postgres.close() # 1

def etl_to_mmr_dim_products(): # etl from ra-db.products to mmr.dimension_products
    try:
        conn_postgres = get_inovus_odb_p_connection() # 1
        cur_p = conn_postgres.cursor() # 1
        cur_p.execute("select * from odb_inovus.products;") # 1
        rows = cur_p.fetchall() # 1
        conn_inovus = get_inovus_i_connection() # 2
        cur_i = conn_inovus.cursor() # 2
        cur_i.executemany('insert into mrr.dimension_products values (%s, %s, %s)', rows) # 2
        create_log_suc('etl_to_mmr_dim_products')
    except:
        create_log_er('etl_to_mmr_dim_products')
        raise Exception
    conn_inovus.commit() # 2
    conn_inovus.close() # 2
    conn_postgres.close() # 1

def update_high_water_mark():
    conn_inovus = get_inovus_i_connection()
    cur_i = conn_inovus.cursor()
    cur_i.execute("update dwh.high_water_mark SET date_update = now() WHERE name_db = 'mrr';")
    conn_inovus.commit()
    conn_inovus.close()

with DAG(
    dag_id='inovus_etl_odb_to_mrr',
    schedule_interval='@daily',
    start_date=days_ago(2),
    tags=['etl']
    ) as dag:
    
    task_sales = PythonOperator(
        task_id = 'etl_odb_to_mrr_f_sales',
        python_callable = etl_to_mmr_f_sale
    )

    task_customer = PythonOperator(
        task_id = 'etl_odb_to_mrr_dim_customer',
        python_callable = etl_to_mmr_dim_customer
    )

    task_products = PythonOperator(
        task_id = 'etl_odb_to_mrr_dim_products',
        python_callable = etl_to_mmr_dim_products
    )

    task_high_water_mark = PythonOperator(
        task_id = 'date_update_mrr',
        python_callable = update_high_water_mark
    )

    task_sales >> task_customer >> task_products >> task_high_water_mark 

