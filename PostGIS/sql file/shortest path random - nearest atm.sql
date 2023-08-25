Drop table if exists way_result;
Create table if not exists way_result 
As (
	SELECT 
		ST_LENGTH(ST_GeomFromText(res.st_astext ,4326)::geography)/1000 as distance_km,
		ST_GeomFromText(res.st_astext ,4326) as geom_path
	FROM (
		-- find he nearest vertex to the start longitude/latitude
		WITH start_point AS (
  		SELECT topo.source --could also be topo.target
  		FROM hanoi_routing as topo
  		ORDER BY topo.geom_way <-> ST_GeomFromText('POINT (105.8236653 21.0221486)', 4326)
  		LIMIT 1
		),
		-- find the nearest vertex to the destination longitude/latitude
		destination AS (
  		SELECT topo.source --could also be topo.target
		FROM hanoi_routing as topo, atm_table as atm
		WHERE atm.id IN (
			Select atm.id
			From atm_table atm
			Order by ST_Distance(way, ST_Transform(ST_GeomFromText('POINT (105.8236653 21.0221486)', 4326),3857))
			LIMIT 1
			)
		ORDER BY topo.geom_way <-> ST_Transform(atm.way, 4326)
		LIMIT 1
		)
		-- use Dijsktra and join with the geometries
		SELECT ST_AsText(ST_Union(geom_way))
		FROM pgr_dijkstra('
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
  			ON di.edge = pt.id
		ORDER BY ST_LENGTH(ST_Union(geom_way))
  		LIMIT 1
	) as res
)