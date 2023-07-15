import psycopg2.extras

hostname = "localhost"
database = "postgres"
username = "postgres"
pwd = "08062001"
port_id = 5432

conn = None
cur = None

try:
    with psycopg2.connect(dbname=database, user=username, password=pwd, host=hostname, port=port_id) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('DROP TABLE IF EXISTS public.test')
            create_test_table = '''
                        CREATE TABLE IF NOT EXISTS public.test(
                        id  int PRIMARY KEY,
                        name text,
                        way geometry(Point, 3857),
                        queue smallint
                        )
                        '''
            cur.execute(create_test_table)
            insert_script = 'INSERT INTO public.test (id, name, way, queue) VALUES (%s,%s,%s,%s)'
            insert_values = [(1, "BIDV", "0101000020110F00004DB21C43EE7D664194DEDEDA303E4241", 0),
                             (2, "Sacombank", "0101000020110F0000F7B90548A07A664187B92065483C4241", 0),
                             (3, "Public Bank", "0101000020110F0000189C084A127B6641744C3C28D9384241", 0),
                             (4, 'Dongabank - ATM', '0101000020110F00007EC36AC87F776641D0049AB42F434241', 0)]
            for record in insert_values:
                cur.execute(insert_script, record)
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
