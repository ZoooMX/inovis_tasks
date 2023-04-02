-- ============================== оперативная БД   
create schema if not exists odb_inovus;

drop table if exists odb_inovus.sales;
create table if not exists odb_inovus.sales (
	custumer_id bigint not null,
	product_id bigint not null,
	qty varchar(255)
);

drop table if exists odb_inovus.customer;
create table if not exists odb_inovus.customer (
	id bigint not null,
	"name" varchar(255),
	country varchar (255)
);

drop table if exists odb_inovus.products;
create table if not exists odb_inovus.products (
	id bigint not null,
	"name" varchar(255),
	groupname varchar(255)
);

-- наполнение БД
insert into odb_inovus.sales (custumer_id, product_id, qty)
values 
(1, 11, 'buy'),
(2, 22, 'test'),
(3, 33, 'preorder'),
(4, 44, 'test'),
(5, 55, 'test'),
(6, 66, 'test'),
(7, 77, 'preorder'),
(8, 77, 'preorder'),
(2, 77, 'buy'),
(3, 77, 'preorder'),
(2, 22, 'buy'),
(1, 33, 'buy'),
(4, 44, 'buy'),
(8, 11, 'buy'),
(5, 11, 'buy'),
(7, 77, 'preorder'),
(7, 33, 'buy'),
(3, 44, 'buy'),
(2, 77, 'preorder'),
(2, 88, 'buy')
;

insert into odb_inovus.customer (id, "name", country)
values 
(1, 'Andy', 'Canada'),
(2, 'Alex', 'Turkish'),
(3, 'Din', 'England'),
(4, 'Max', 'USA'),
(5, 'Gregory', 'Russia'),
(6, 'Petr', 'Turkish'),
(7, 'Max', 'USA'),
(8, 'Eva', 'England')
;

insert into odb_inovus.products (id, "name", groupname)
values 
(11, 'Iphone', 'phone'),
(22, 'Macbook_air', 'laptop'),
(33, 'RedmiA1', 'phone'),
(44, 'AsusROG', 'laptop'),
(55, 'Ipad_air', 'tablet'),
(66, 'HPomen', 'laptop'),
(77, 'Macbook_pro', 'laptop'),
(88, 'Ipad_pro', 'tablet')
;