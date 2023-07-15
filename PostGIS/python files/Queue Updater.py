import psycopg2.extras
import time
from queue_generator import queue_gen, busy_gen

hostname = "localhost"
database = "postgres"
username = "postgres"
pwd = "08062001"
port_id = 5432

conn = None
cur = None

try:
    print('Generator Started !')
    while True:
        try:
            with psycopg2.connect(dbname=database, user=username, password=pwd, host=hostname, port=port_id) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    # Get number of ATM
                    # Update number if new records of ATM are inserted
                    cur.execute('Select Count(*) from public.atm_table')
                    rows = cur.fetchall()[0][0]
                    # Generate a queue for every ATM
                    for i in range(1, rows + 1):
                        cur.execute('UPDATE public.atm_table SET queue = %s WHERE id = %s', [queue_gen(busy_gen()), i])
        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        print("Values Updated !")
        time.sleep(15)
except KeyboardInterrupt:
    print('Generator Stopped !')
