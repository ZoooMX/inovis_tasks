-- показывает дубли по колонке(id) и выбранной таблице 
-- при обработке данных в stg необходимо избавиться от дублей в измерениях

create or replace procedure dwh.find_double_id_cout(name_cal_1 varchar, name_cal_2 varchar, name_t varchar) as
$$
declare 
	my_cursor refcursor; -- объявлена переменная курсора
	result record;
 	query text := ('select '|| name_cal_1 ||', "name", '|| name_cal_2 ||', count(*) from '|| name_t ||' group by '|| name_cal_1 ||', "name", '|| name_cal_2 ||' having count(*) > 1');
begin
	open my_cursor for execute query;
	fetch my_cursor into result;
	raise notice 'Info dublicate: % %', result, now();
	while found
	loop
		fetch my_cursor into result;
		raise notice 'Info dublicate: % %', result, now();
	end loop;
	close my_cursor;
end;
$$
language plpgsql;

call dwh.find_double_id_cout('id', 'country','stg.dimension_customer');
call dwh.find_double_id_cout('id', 'groupname','stg.dimension_products');