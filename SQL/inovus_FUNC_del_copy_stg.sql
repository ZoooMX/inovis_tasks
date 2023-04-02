-- функция удаляющая копии записей в таблице stg.dimension_customer
create or replace function dwh.del_double_cus() 
returns setof stg.dimension_customer as  
$$
begin
	delete from stg.dimension_customer
	where ctid not in (
 	select max(ctid)
  	from stg.dimension_customer
  	group by id, "name", country
);
end;
$$ 
language plpgsql;

--проверка
--insert into stg.dimension_customer (id, "name", country)
--values 
--(7, 'Max', 'USA'),
--(8, 'Eva', 'England');
--select dwh.del_double_cus();
--select * from stg.dimension_customer;


-- функция удаляющая копии записей в таблице stg.dimension_products
create or replace function dwh.del_double_prod() 
returns setof stg.dimension_products as  
$$
begin
	delete from stg.dimension_products
	where ctid not in (
 	select max(ctid)
  	from stg.dimension_products
  	group by id, "name", groupname
);
end;
$$ 
language plpgsql;

-- проверка
--insert into stg.dimension_products (id, "name", groupname)
--values 
--(77, 'Macbook_pro', 'laptop'),
--(88, 'Ipad_pro', 'tablet');
--select dwh.del_double_prod();
--select * from stg.dimension_products;



