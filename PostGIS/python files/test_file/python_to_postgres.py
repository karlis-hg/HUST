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
            # cur.execute('DROP TABLE IF EXISTS public.test_table')
            # create_script = '''
            # CREATE TABLE IF NOT EXISTS public.test_table(
            # id  int PRIMARY KEY,
            # name varchar(40) NOT NULL,
            # test_num int
            # )
            # '''
            #
            # cur.execute(create_script)
            #
            insert_script = 'INSERT INTO public.test_table (id, name, test_num) VALUES (%s,%s,%s)'
            insert_values = [(1, "Pengu", 86), (2, "Pengi", 861), (3, "Penga", 186)]
            print(type(insert_values))
            # for record in insert_values:
            #     cur.execute(insert_script, record)
            #
            # update_script = 'UPDATE public.test_table SET test_num = test_num + (test_num * 0.4)'
            # cur.execute(update_script)
            #
            # cur.execute("Select * From public.test_table")
            # for record in cur.fetchall():
            #     print(record['name'], record['test_num'])
            find_atm = '''
            Select point.name, point.operator 
            From planet_osm_point point
            Where point.amenity = 'atm' and (point.name is not null or point.operator is not null) 
            '''
            cur.execute(find_atm)
            # for record in cur.fetchall():
            #     print(record['name'], record['operator'])
            print(len(cur.fetchall()))
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
