#import pymssql


class SQLServerDatabase:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def execute_query(self, query):
        try:
            # Establish a connection to the SQL Server database
            #connection = pymssql.connect(self.server, self.username, self.password, self.database)

            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # Execute the SQL query
            cursor.execute(query)

            # Fetch all results
            result = cursor.fetchall()

            # Close the cursor and the connection
            cursor.close()
            connection.close()

            return result

        except Exception as e:
            print(f"Error executing SQL query: {str(e)}")
            return None
