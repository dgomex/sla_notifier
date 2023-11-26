import pymssql


class SQLServerDatabase:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def execute_query(self, query):
        try:
            with pymssql.connect(self.server, self.username, self.password, self.database) as conn:
                with conn.cursor(as_dict=True) as cursor:
                    cursor.execute(query)
            return cursor

        except Exception as e:
            print(f"Error executing SQL query: {str(e)}")
            return None
