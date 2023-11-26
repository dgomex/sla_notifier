import os
import pymssql

with pymssql.connect(os.getenv("AC_SERVER"),
                     os.getenv("AC_USERNAME"),
                     os.getenv("AC_PASSWORD"),
                     os.getenv("AC_DB")) as conn:
    with conn.cursor(as_dict=True) as cursor:
        cursor.execute("SELECT 1")
