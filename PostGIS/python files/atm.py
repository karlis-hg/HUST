import psycopg2.extras
import constants as cst


def name_picker(name, operator):
    res = name
    if res is None:
        res = operator
    return res


hostname = cst.hostname
database = cst.database
username = cst.username
pwd = cst.password
port_id = cst.port_id

conn = None
cur = None
i = 1
insert_values = []

try:
    with psycopg2.connect(dbname=database, user=username, password=pwd, host=hostname, port=port_id) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Find all atm that has value in name or operator column
            find_atm = '''
            Select name, operator, way
            From planet_osm_point
            Where ST_Contains(ST_Transform(ST_GeomFromText('POLYGON(( 105.7758 20.9497, 105.9388 20.9497, 
                                                                      105.9388 21.0813, 105.7758 21.0813,   
                                                                      105.7758 20.9497))', 4326), 3857), way)
            and amenity = 'atm' and (name is not null or operator is not null) 
            '''
            cur.execute(find_atm)
            atm_found = cur.fetchall()
            # Extract one name only and its geo attribute for each atm found
            # Create Insert Records consist of id, name, point and current queue
            for record in atm_found:
                record_tmp = [i, name_picker(record['name'], record['operator']), record['way'], 0]
                i += 1
                insert_values.append(tuple(record_tmp))
            # print(len(insert_values))
            # print(insert_values)

            # Create Hanoi ATM only table
            cur.execute('DROP TABLE IF EXISTS public.atm_table')
            create_atm_table = '''
            CREATE TABLE IF NOT EXISTS public.atm_table(
            id  int PRIMARY KEY,
            name text,
            way geometry(Point, 3857),
            queue smallint
            );
            CREATE INDEX IF NOT EXISTS idx_location ON atm_table(id, way)
            '''
            cur.execute(create_atm_table)
            # Insert created values into table
            insert_script = 'INSERT INTO public.atm_table (id, name, way, queue) VALUES (%s, %s,%s,%s)'
            for record in insert_values:
                cur.execute(insert_script, record)

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
