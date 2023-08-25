SELECT 
		ST_LENGTH(ST_GeomFromText(res.st_astext ,4326)::geography)/1000 as distance_km,
		ST_GeomFromText(res.st_astext ,4326) as geom_path
	FROM (
		-- find he nearest vertex to the start longitude/latitude
		WITH start_point AS (
  		SELECT topo.source --could also be topo.target
  		FROM hanoi_routing as topo
  		ORDER BY topo.geom_way <-> ST_GeomFromText('POINT (105.8237175 21.0221134)', 4326)
  		LIMIT 1
		),
		-- find the nearest vertex to the destination longitude/latitude
		destination AS (
  		SELECT topo.source --could also be topo.target
		FROM hanoi_routing as topo, atm_table as atm
		WHERE atm.id IN (
			Select atm.id
			From atm_table atm
			Order by ST_Distance(way, ST_Transform(ST_GeomFromText('POINT (105.8237175 21.0221134)', 4326),3857))
			LIMIT 1
			)
		ORDER BY topo.geom_way <-> ST_Transform(atm.way, 4326)
		LIMIT 1
		),
		nearest_atm AS (
		Select ST_Transform(atm.way, 4326) as stop_p
		From atm_table atm
		Order by ST_Distance(way, ST_Transform(ST_GeomFromText('POINT (105.8237175 21.0221134)', 4326),3857))
		LIMIT 1
		)
		-- use Dijsktra and join with the geometries
		SELECT ST_AsText(ST_Union(main_route.geom_way, finishing_line.way))
		FROM 
		(	pgr_dijkstra('
    		SELECT id,
        		source,
         		target,
         		cost,
				reverse_cost,
		 		x1, y1, x2, y2
				FROM hanoi_routing',
    		array(SELECT source FROM start_point),
    		array(SELECT source FROM destination),
    		directed := true) AS di
			JOIN hanoi_routing AS pt
  			ON di.edge = pt.id ) AS main_route,
		(	SELECT ST_Union(
				ST_MakeLine(last_vertex.start_p, atm.stop_p),
				ST_MakeLine(gps.start_p, first_vertex.stop_p))as way
			FROM 
		 	(	SELECT stop_p from nearest_atm
				) AS atm,
			(	SELECT hnv.geom_vertex as start_p
				FROM hanoi_vertex hnv
				WHERE id IN (SELECT source FROM destination)
				) AS last_vertex,
			(	SELECT hnv.geom_vertex as stop_p
				FROM hanoi_vertex hnv
				WHERE id IN (SELECT source FROM start_point)
				) AS first_vertex,
		 	(	Select ST_GeomFromText('POINT (105.8237175 21.0221134)', 4326) as start_p
				) AS gps
		) as finishing_line
	) as res