Drop table if exists hanoi_routing;
Create table if not exists hanoi_routing 
As (Select * From at_2po_4pgr
	Where ST_Contains(ST_Transform(ST_GeomFromText('POLYGON(( 
			105.7758 20.9497, 
			105.9388 20.9497, 
			105.9388 21.0813, 
			105.7758 21.0813,	
			105.7758 20.9497))', 4326), 4326), geom_way));
