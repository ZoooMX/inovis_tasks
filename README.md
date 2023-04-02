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
#### Задача_1.
Создать оперативную базу данных в любом из видов баз данных(не важно реляционной или нет) 3 таблицы:
а. Таблица продаж - sales : customerId, productId, qty
б. Таблица клиентов - customers: id, name, country
в. Таблица продуктов- products : id, name, groupname

##### Процесс выполнения 
БД разворачивал в Docker 
**Скрипт DLL и DML комманд -> [inovus_ODB.sql](https://github.com/ZoooMX/inovus_tasks/blob/main/SQL/inovus_ODB.sql)**

Было принято решение использовать для оперативной базы данных PostgreSQL. Данная БД использвуется очень широко на рынке, часто ее используют на бэкенде(пообщался с знакомими програмистами) Основные отличия приведены в таблице ниже.
![image](https://user-images.githubusercontent.com/99000578/229366000-0508f3ae-fe2f-475b-8231-3d4a40196371.png)


#### Задача_2.
Создать дополнительные три базы данных на другом инстансе от оперативной (обязательно реляционная mysql, postgresql, etc….):
mrr, stg, dwh - нужно почитать и понять почему мы строим 3 базы и для чего каждая из них

##### Процесс выполнения 
БД разворачивал в Docker. В DLL коммандах для DWH построены связи для дальнейшей работы в BI. 
**Скрипт DLL и DML комманд -> [inovus_MRR_STG_DWH.sql](https://github.com/ZoooMX/inovus_tasks/blob/main/SQL/inovus_MRR_STG_DWH.sql)**
- mrr - Monthly Recurring Revenue - ежемесячныя выгрузка данных в данную БД для дальнейшей работы с показателмя за прошедший месяц. 
Думаю сюда выгружаются все данные из всех доступных источниов
- stg - Staging - БД для отладки данных, куда можно сгрузить даже поврежденные данные, так же в ней осуществляется обработка данных(преобразование)
- dwh - Data Warehouse - БД с переработанными данными, готовыми для подготовки бизнес-анализа и отчетов для дальнейшего принятия решений бизнесом
