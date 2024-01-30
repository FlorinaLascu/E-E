import psycopg2

__conn = None

def get_sql_conn():
    global __conn
    if __conn is None:
        conn = psycopg2.connect(database="e&e",
                        host="localhost",
                        user="postgres",
                        password="postgres")
        return conn