/* new instance zone - docker postgres


mrr - Monthly Recurring Revenue - ежемесячныя выгрузка данных в данную БД для дальнейшей работы с показателмя за прошедший меесяц. 
Думаю сюда прилетают все данные из всех доступных источниов

stg - Staging - БД для отладки данных, куда можно сгрузить даже поврежденные данные, так же в ней осуществляется обработка данных(преобразование) 

dwh - Data Warehouse БД с переработанными данными готовыми для подготовки бизнес-анализа и отчетов для дальнейшего принятия решений бизнесом 
*/

-- ============================== MRR
create schema if not exists mrr; 

drop table if exists mrr.fact_sales;
create table if not exists mrr.fact_sales (
	custumer_id bigint,
	product_id bigint,
	qty varchar(255)
);

drop table if exists mrr.dimension_customer;
create table if not exists mrr.dimension_customer (
	id bigint,
	"name" varchar(255),
	country varchar (255)
);

drop table if exists mrr.dimension_products;
create table if not exists mrr.dimension_products (
	id bigint,
	"name" varchar(255),
	groupname varchar(255)
);

-- ============================== STG
create schema if not exists stg; 

drop table if exists stg.fact_sales;
create table if not exists stg.fact_sales (
	custumer_id bigint,
	product_id bigint,
	qty varchar(255)
);

drop table if exists stg.dimension_customer;
create table if not exists stg.dimension_customer (
	id bigint,
	"name" varchar(255),
	country varchar (255)
);

drop table if exists stg.dimension_products;
create table if not exists stg.dimension_products (
	id bigint,
	"name" varchar(255),
	groupname varchar(255)
);	
	
-- ============================== DWH
create schema if not exists dwh; 

drop table if exists dwh.dimension_customer;
create table if not exists dwh.dimension_customer (
	id bigint not null unique,
	"name" varchar(255),
	country varchar (255),
	constraint PK_1 primary key (id)
);

drop table if exists dwh.dimension_products;
create table if not exists dwh.dimension_products (
	id bigint not null unique,
	"name" varchar(255),
	groupname varchar(255),
	constraint PK_2 primary key (id)
);	

drop table if exists dwh.fact_sales;
create table if not exists dwh.fact_sales (
	customer_id bigint,
	product_id bigint,
	qty varchar(255),
	constraint FK_1 foreign key (customer_id) references dwh.dimension_customer (id),
	constraint FK_2 foreign key (product_id) references dwh.dimension_products (id)
);


-- ============================== 
-- запись последнего переноса данных с odb в mmr и в dwh
drop table if exists dwh.high_water_mark;
create table if not exists dwh.high_water_mark (
	name_db varchar(50),
	date_update timestamp
);



