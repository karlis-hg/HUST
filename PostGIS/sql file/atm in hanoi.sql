SELECT * FROM planet_osm_point   
WHERE   
   ST_Contains(ST_Transform(ST_GeomFromText('POLYGON(( 
        	105.7758 20.9497, 
        	105.9388 20.9497, 
        	105.9388 21.0813, 
        	105.7758 21.0813,	
        	105.7758 20.9497))', 4326), 3857), way)  
AND amenity= 'atm' and (name is not null or operator is not null)

