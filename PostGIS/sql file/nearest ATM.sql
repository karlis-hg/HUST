Drop table if exists test_2;
Create table if not exists test_2
As
Select *, ST_Distance(way, ST_Transform(ST_SetSRID(ST_Point(105.8421920, 21.0041939),4326),3857)) as dist
From atm_table
Order by dist
Limit 5;

Delete from test_2 Where id = 0;

Insert into test_2 (id, name, way, queue, dist)
Values (0, 'D4 Hust', ST_Transform(ST_SetSRID(ST_Point(105.8421920, 21.0041939),4326),3857), 0, 0);



Select * from test_2
Order by dist;
