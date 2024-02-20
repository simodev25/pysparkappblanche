from helpers.db.postgres import PostGresDBManager
class ConsoRepository(PostGresDBManager):
    def insert_total_volume(self, interval_timestamp, pce, total_volume):
        # Method to insert consumption data into the database

        if self.conn is not None:
            try:
                with self.conn.cursor() as cursor:
                    query = """
                    INSERT INTO volume_total (interval_timestamp, pce, total_volume)
                    VALUES (%s, %s, %s);
                    """
                    cursor.execute(query, (interval_timestamp, pce, total_volume))
            except Exception as e:
                print(f"Failed to insert consumption data: {e}")
        else:
            print("Database connection is not established.")