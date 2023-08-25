import constants as cst
import psycopg2.extras
import random


def modify_point(gps):
    lat, long = gps.split(',')  # Extract vĩ độ, kinh độ
    return "POINT (" + long + " " + lat + ")"


def travel_time(length, MoT_speed):
    length = length / 1000
    return round(length / MoT_speed * 60)  # t = s/v (minutes)


def wait_time(travel, queue):
    wait = 0
    if queue > 0:
        for i in range(1, queue + 1):
            wait += random.randint(3, 5)
    return max(wait - travel, 0)


hostname = cst.hostname
database = cst.database
username = cst.username
pwd = cst.password
port_id = cst.port_id
conn = None
cur = None
idx = 0
result_tmp = []

speed_dict = {
    "Walk": 5,
    "Bike": 12,
    "Motor": 30,
    "Car": 45
}

query_dict = {
    "dist": "ORDER BY rr.distance",
    "queue": "ORDER BY rr.queue, rr.distance",
    "wait": "ORDER BY rr.wait, rr.distance"
}

query_type = cst.QUERY_TYPE
limit = cst.LIMIT_RANGE
position = modify_point(cst.POSITION)
speed = speed_dict[cst.MEAN_OF_TRANSPORT]

try:
    with psycopg2.connect(dbname=database, user=username, password=pwd, host=hostname, port=port_id) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Find nearest atms by Euclides distance
            find_atms = '''
            WITH beginning AS (Select ST_GeomFromText(%s, 4326) as way)
            SELECT atm.id, atm.way, atm.queue
            FROM atm_table atm, beginning
            ORDER BY ST_Distance(atm.way, ST_Transform(beginning.way, 3857))
            LIMIT %s
            '''
            cur.execute(find_atms, [position, limit])
            atms_found = cur.fetchall()
            # Result table to store all route found
            create_result_table = '''
            DROP TABLE IF EXISTS public.route_results;
            CREATE TABLE IF NOT EXISTS public.route_results(
            idx  smallint PRIMARY KEY,
            distance float,
            queue smallint,
            wait float,
            way geometry(MultiLineString, 4326)            
            );
            CREATE INDEX IF NOT EXISTS idx ON route_results(idx)
            '''
            insert_result = 'INSERT INTO route_results (idx, distance, queue, wait, way) VALUES (%s, %s, %s, %s, %s)'
            cur.execute(create_result_table)

            # Path to ATM (2 ways)
            path_to_atm = '''
            WITH beginning AS (Select ST_GeomFromText(%s, 4326) as way),
                 atm AS (Select ST_Transform(%s, 4326) as way)
	        SELECT ST_LENGTH(ST_Union(res.path)::geography) as distance_meter,
		           ST_Union(res.path) as geom_path
	        FROM (
		        -- find he nearest vertex to the start longitude/latitude
		        WITH start_point AS (
  		        SELECT topo.source --could also be topo.target
  		        FROM hanoi_routing as topo, beginning
  		        ORDER BY topo.geom_way <-> beginning.way
  		        LIMIT 1),
		        -- find the nearest vertex to the destination longitude/latitude
		        destination AS (
  		        SELECT topo.source --could also be topo.target
		        FROM hanoi_routing as topo, atm
		        ORDER BY topo.geom_way <-> atm.way
		        LIMIT 1)
		        -- use Dijkstra and join with the geometries
		        SELECT ST_Union(main_route.geom_way, finishing_line.way) as path
		        FROM
                (   pgr_dijkstra('SELECT id, source, target, cost, reverse_cost, x1, y1, x2, y2 FROM hanoi_routing',
                	                array(SELECT source FROM start_point),
                	                array(SELECT source FROM destination),
                	                directed := true) AS di
                	JOIN hanoi_routing AS pt
                	ON di.edge = pt.id
                    ) AS main_route,
                (	SELECT ST_Union(
            		ST_MakeLine(last_vertex.start_p, atm.way),
            		ST_MakeLine(beginning.way, first_vertex.stop_p)) AS way
            	    FROM
             	    beginning,
             	    atm,
            	    (   SELECT hnv.geom_vertex as start_p
            		    FROM hanoi_vertex hnv
            		    WHERE id IN (SELECT source FROM destination)
            		    ) AS last_vertex,
            	    (	SELECT hnv.geom_vertex as stop_p
            		    FROM hanoi_vertex hnv
            		    WHERE id IN (SELECT source FROM start_point)
            		    ) AS first_vertex
                    ) AS finishing_line
	            ) as res
                '''

            path_to_atm_alt = '''
            SELECT ST_LENGTH(ST_Multi(ST_MakeLine(b.start_p, e.stop_p))::geography) as distance_meter,
	               ST_Multi(ST_MakeLine(b.start_p, e.stop_p)) as geom_path
            FROM (Select ST_GeomFromText(%s, 4326) as start_p) b,
	             (Select ST_Transform(%s, 4326) as stop_p) e
            '''

            for atm in atms_found:
                idx = atm['id']
                cur.execute(path_to_atm, [position, atm['way']])
                result = cur.fetchall()[0]
                dist = result['distance_meter']
                geom = result['geom_path']
                if (dist, geom) == (None, None):
                    cur.execute(path_to_atm_alt, [position, atm['way']])
                    result = cur.fetchall()[0]
                    dist = result['distance_meter']
                    geom = result['geom_path']
                # print(atm['queue'], dist, geom)
                record = [idx, round(dist), atm['queue'], wait_time(travel_time(dist, speed), atm['queue']), geom]
                # result_tmp.append(record)
                cur.execute(insert_result, tuple(record))

            order = query_dict[query_type]
            extract = "SELECT * FROM route_results rr " + order + " LIMIT 1"
            display_route = '''
            DROP TABLE IF EXISTS public.way_result;
            CREATE TABLE IF NOT EXISTS public.way_result AS (
            SELECT ST_GeomFromText(%s, 4326) as depart, atm.way as arrive, rr.way as path
            FROM atm_table atm, route_results rr
            WHERE atm.id = rr.idx 
            ''' + order + " LIMIT 1 )"
            cur.execute(display_route, [position])
            cur.execute(extract)
            display_stat = cur.fetchall()[0]
            print("Mean of Transport:", cst.MEAN_OF_TRANSPORT, "({} km/h)".format(speed))
            print("Distance:", display_stat['distance'], "m")
            print("Travel Time:", travel_time(display_stat['distance'], speed), "minutes")
            print("Current Queue:", display_stat['queue'], "people")
            print("Estimated Wait Time:", display_stat['wait'], "minutes")
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
