# inovus_tasks
## Отчет по выполнению тестового задания Inovas

### Перечень задач:
1. Создать оперативную базу данных в любом из видов баз данных(не важно реляционной или нет)  3 таблицы:
а. Таблица продаж - sales : customerId, productId, qty
б. Таблица клиентов - customers: id, name, country
в. Таблица продуктов- products : id, name, groupname


2. Создать дополнительные три базы данных на другом инстансе от оперативной (обязательно реляционная mysql, postgresql, etc….):
mrr, stg, dwh - нужно почитать и понять почему мы строим 3 базы и для чего каждая из них

3. Во все таблицы с мерами мы добавляем приставку fact в имени, c измерениями  dimension + приставка имени базы данных. Пример: если таблица в базе данных mrr то таблица с продажами будет mrr_fact_sales, если таблица с продуктами в stg то stg_dim_products. В именах только английский, и все имена одного формата(камел кейс или снейк кейс).Почитать что такое fact и dimension

4. Создать ETL(airflow, nifi, spark, SSIS либо любой другой ETL) с переходами данными из оперативной базы в mrr -> stg -> dwh 
Из оперативной базы данных в mrr брать данные с помощью high water mark(дельта).Для этого создать таблицу high_water_mark в который будет последний день или апдейт каждой таблицы. В mrr вытягиваем в параметр время в соответствии с таблицей источникам и в dwh обновляем high_water_mark последним значением которое есть в таблице.

5. В каждом пакете/даге/процессе сделать систему логов которые будут писаться в созданную для этого таблицу, время исполнения пакета + если есть ошибка(это делаеться в event handler)

6. Создать процедуру и использовать там cursor, try и catch(при ошибки будет писаться лог в созданную для этого таблицу), сделать какую нибудь функцию.
Все процедуры и функции сохранить в базе данных dwh.


7. Сделать простой дашборд и модель данных на ваше усмотрение в Power BI из данных в dwh.

8. Создать скрипт который будет делать backup для трех баз данных(mrr, stg, dwh).

### Выполнение: 
### Задача_1.
Создать оперативную базу данных в любом из видов баз данных(не важно реляционной или нет) 3 таблицы:
а. Таблица продаж - sales : customerId, productId, qty
б. Таблица клиентов - customers: id, name, country
в. Таблица продуктов- products : id, name, groupname

##### Процесс выполнения 
БД разворачивал в Docker 
**Скрипт DLL и DML комманд -> [inovus_ODB.sql](https://github.com/ZoooMX/inovus_tasks/blob/main/SQL/inovus_ODB.sql)**

Было принято решение использовать для оперативной базы данных PostgreSQL. Данная БД использвуется очень широко на рынке, часто ее используют на бэкенде(пообщался с знакомими програмистами) Основные отличия приведены в таблице ниже.
![image](https://user-images.githubusercontent.com/99000578/229366000-0508f3ae-fe2f-475b-8231-3d4a40196371.png)



### Задача_2.
Создать дополнительные три базы данных на другом инстансе от оперативной (обязательно реляционная mysql, postgresql, etc….):
mrr, stg, dwh - нужно почитать и понять почему мы строим 3 базы и для чего каждая из них

##### Процесс выполнения 
БД разворачивал в Docker. В DLL коммандах для DWH построены связи для дальнейшей работы в BI. 
**Скрипт DLL комманд -> [inovus_MRR_STG_DWH.sql](https://github.com/ZoooMX/inovus_tasks/blob/main/SQL/inovus_MRR_STG_DWH.sql)**
- mrr - Monthly Recurring Revenue - ежемесячныя выгрузка данных в данную БД для дальнейшей работы с показателмя за прошедший месяц. 
> Думаю сюда выгружаются все данные из всех доступных источниов
- stg - Staging - БД для отладки данных, куда можно сгрузить даже поврежденные данные, так же в ней осуществляется обработка данных(преобразование)
- dwh - Data Warehouse - БД с переработанными данными, готовыми для подготовки бизнес-анализа и отчетов для дальнейшего принятия решений бизнесом.

### Задача_3.
Во все таблицы с мерами мы добавляем приставку fact в имени, c измерениями  dimension + приставка имени базы данных. Пример: если таблица в базе данных mrr то таблица с продажами будет mrr_fact_sales, если таблица с продуктами в stg то stg_dim_products. В именах только английский, и все имена одного формата(камел кейс или снейк кейс).Почитать что такое fact и dimension

##### Процесс выполнения 
**Скрипт DLL комманд -> [inovus_MRR_STG_DWH.sql](https://github.com/ZoooMX/inovus_tasks/blob/main/SQL/inovus_MRR_STG_DWH.sql)**
- dimension - таблицы с измерениями, которые содержат описание о значениях в таблице фактов.  
- fact - фактичкские данные(количество товаров, цена и т.д.) имеющие прямую связь с таблицами измерений для дальнейшего анализа данных. 
Пример указан на картинке ниже
<img width="440" alt="image" src="https://user-images.githubusercontent.com/99000578/229367611-2d08dd66-bc7c-4825-a769-14bd82bb5c00.png">

### Задача_4.
Создать ETL(airflow, nifi, spark, SSIS либо любой другой ETL) с переходами данными из оперативной базы в mrr -> stg -> dwh 
Из оперативной базы данных в mrr брать данные с помощью high water mark(дельта).Для этого создать таблицу high_water_mark в который будет последний день или апдейт каждой таблицы. В mrr вытягиваем в параметр время в соответствии с таблицей источникам и в dwh обновляем high_water_mark последним значением которое есть в таблице.
##### Процесс выполнения 
Выбрал инструмент для реализации ETL - Apache Airflow. Запуск осуществлялся через Docker, параметры запуска [Docker-compose.yaml](https://github.com/ZoooMX/inovus_tasks/blob/main/airflow/docker-compose.yaml).     
1. Python скрипт [ETL ODB -> MRR -> high_water_mark](https://github.com/ZoooMX/inovus_tasks/blob/main/airflow/dags/inovus_etl_odb_mrr.py)
2. Python скрипт [ETL MRR -> STG](https://github.com/ZoooMX/inovus_tasks/blob/main/airflow/dags/inovus_etl_mrr_stg.py)
3. Python скрипт [ETL STG -> DWH -> high_water_mark](https://github.com/ZoooMX/inovus_tasks/blob/main/airflow/dags/inovus_etl_stg_dwh.py)
- **Скрин Airflow с DAG** <img width="918" alt="image" src="https://user-images.githubusercontent.com/99000578/229368243-df4563c6-fff7-4577-8422-cfe040bc019c.png">
- **ETL ODB -> MRR -> high_water_mark** ![image](https://user-images.githubusercontent.com/99000578/229368631-08617d27-d522-48b5-b51d-ab9367fd2b1e.png)
- **ETL MRR -> STG** ![image](https://user-images.githubusercontent.com/99000578/229368659-12ad80b9-e19d-4482-a7ae-9449caf657fe.png)
- **ETL STG -> DWH -> high_water_mark** ![image](https://user-images.githubusercontent.com/99000578/229369392-ada38374-011a-4072-a17d-37da24da7072.png)
- **Запись в high_water_mark** <img width="340" alt="image" src="https://user-images.githubusercontent.com/99000578/229369435-0f07dc40-4ce0-417b-a78f-385b92bb2883.png">


### Задача_5.
В каждом пакете/даге/процессе сделать систему логов которые будут писаться в созданную для этого таблицу, время исполнения пакета + если есть ошибка(это делаеться в event handler).
##### Процесс выполнения 
Развернул отдельную базу данных(отдельный инстанс через Docker), так как ETL частый процесс и логи будут копиться быстро и большом количестве, что может создать нагрузку и лишний риск на dwh базу. Очень эффективно вести логирование в колночной БД, к сожалению не имея опыта за реализацию в Clickhouse не брался. 
Систему логов реализовал через исключения с записью в таблицу информации об успешном или ошибки выполнении task в Airflow.
1. Python скрипт [ETL ODB -> MRR -> high_water_mark](https://github.com/ZoooMX/inovus_tasks/blob/main/airflow/dags/inovus_etl_odb_mrr.py)
2. Python скрипт [ETL MRR -> STG](https://github.com/ZoooMX/inovus_tasks/blob/main/airflow/dags/inovus_etl_mrr_stg.py)
3. Python скрипт [ETL STG -> DWH -> high_water_mark](https://github.com/ZoooMX/inovus_tasks/blob/main/airflow/dags/inovus_etl_stg_dwh.py)

### Задача_6.
Создать процедуру и использовать там cursor, try и catch(при ошибки будет писаться лог в созданную для этого таблицу), сделать какую нибудь функцию.
Все процедуры и функции сохранить в базе данных dwh.
##### Процесс выполнения 
Реализовал 2 процедуры, которые принимают 2 параметра для поиска дубликатов в stg БД в dimension таблицах. Реализовал 2 функцкии, которые при вызове удаляют дубликаты иставляя одну уникальную запись. Логирование без парсинга CSV файла с встроенными логами Postgres не реализовал, необходимо лучше погрузиться в данный вопрос.  
- процедуры [inovus_PROC_find_double_stg.sql](https://github.com/ZoooMX/inovus_tasks/blob/main/SQL/inovus_PROC_find_double_stg.sql)
- функции [inovus_FUNC_del_copy_stg.sql](https://github.com/ZoooMX/inovus_tasks/blob/main/SQL/inovus_FUNC_del_copy_stg.sql)

### Задача_7.
Сделать простой дашборд и модель данных на ваше усмотрение в Power BI из данных в dwh.
##### Процесс выполнения 
В качестве BI инструмента выбрал Tableau. Данный иснтрумент имеет очень высокую конкуренцию на рынке. Так как я работаю на mac, полноценно использовать без виртуальной машины Power BI нет возможности. В Tableau подключл базу dwh с помощью JDBC драйвера и собрал дашборд. 
- 
#### Задача_8.
Создать скрипт который будет делать backup для трех баз данных(mrr, stg, dwh).
##### Процесс выполнения 
