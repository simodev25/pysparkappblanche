import psycopg2

class PostGresDBManager:
    def __init__(self, conf):
        # Initialize database connection parameters
        self.dbname = conf.get('postgres.dbname')
        self.user = conf.get("postgres.user")
        self.password = conf.get("postgres.password")
        self.host = conf.get('postgres.host')
        self.conn = None

    def set_up(self):
        # Set up the database connection
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.conn.autocommit = True
            print("Database connection established.")
        except Exception as e:
            print(f"Failed to connect to the database: {e}")

    def close(self):
        # Close the database connection
        if self.conn is not None:
            self.conn.close()
            print("Database connection closed.")

    @classmethod
    def get_db_params(self,conf):
        # Simplify database parameter initialization
        return {
            'url': f"jdbc:postgresql://{conf.get('postgres.host')}/{conf.get('postgres.dbname')}",
            'user': conf.get("postgres.user"),
            'password': conf.get("postgres.password"),
            'driver': "org.postgresql.Driver"
        }

