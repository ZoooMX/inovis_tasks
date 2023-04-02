-- логи в отдельную базу так как они будут копиться в больших количествах после каждой таски Airflow
drop table if exists logs.etl_logs;
create table if not exists logs.etl_logs(
	event_time text,
	event_type text,
	message text
	);

select * from logs.etl_logs;