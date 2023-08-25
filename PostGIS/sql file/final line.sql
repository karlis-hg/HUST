WITH nearest_atm AS (
	Select ST_Transform(atm.way, 4326) as stop_p
	From atm_table atm
	Order by ST_Distance(way, ST_Transform(ST_GeomFromText('POINT (105.8236653 21.0221486)', 4326),3857))
	LIMIT 1
)
SELECT ST_Union(ST_MakeLine(last_vertex.start_p, atm.stop_p), ST_MakeLine(depart.start_p, first_vertex.stop_p))
FROM (
	SELECT stop_p from nearest_atm
	) AS atm,
	(
	SELECT hnv.geom_vertex as start_p
	FROM hanoi_vertex hnv
	WHERE id IN (
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
	) AS last_vertex,
	( Select ST_GeomFromText('POINT (105.8236653 21.0221486)', 4326) as start_p
	) As depart,
	(
	SELECT hnv.geom_vertex as stop_p
	FROM hanoi_vertex hnv
	WHERE id IN (
		SELECT topo.source --could also be topo.target
  		FROM hanoi_routing as topo
  		ORDER BY topo.geom_way <-> ST_GeomFromText('POINT (105.8236653 21.0221486)', 4326)
  		LIMIT 1
		)
	) AS first_vertex
	

