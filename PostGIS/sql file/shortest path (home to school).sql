-- find he nearest vertex to the start longitude/latitude
WITH start_point AS (
  SELECT topo.source --could also be topo.target
  FROM hanoi_routing as topo
  ORDER BY topo.geom_way <-> ST_SetSRID(
    ST_GeomFromText('POINT (105.8656595 20.9891936)'),
  4326)
  LIMIT 1
),
-- find the nearest vertex to the destination longitude/latitude
destination AS (
  SELECT topo.source --could also be topo.target
  FROM hanoi_routing as topo
  ORDER BY topo.geom_way <-> ST_SetSRID(
    ST_GeomFromText('POINT (105.8553803 21.0249354)'),
  4326)
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
    directed := false) AS di
JOIN hanoi_routing AS pt
  ON di.edge = pt.id