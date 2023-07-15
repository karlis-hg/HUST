Select *, ST_Distance(way, ST_Transform(ST_SetSRID(ST_Point(105.8421920, 21.0041939),4326),3857)) as dist
From atm_table
Where queue = 0
Order by dist
Limit 5;