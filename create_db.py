import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Connect to default 'postgres' database
        con = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'gbsi'")
        exists = cur.fetchone()
        
        if not exists:
            print("Creating database 'gbsi'...")
            cur.execute('CREATE DATABASE gbsi')
            print("Database 'gbsi' created.")
        else:
            print("Database 'gbsi' already exists.")
            
        cur.close()
        con.close()
        
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
