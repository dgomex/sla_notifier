import os

from sql_server import SQLServerDatabase
from notifier import Notifier
from time import sleep


def main():
    while True:
        try:
            sql_server = SQLServerDatabase(server=os.getenv("AC_SERVER"),
                                           username=os.getenv("AC_USER"),
                                           password=os.getenv("AC_PASSWORD"),
                                           database=os.getenv("AC_DB"))
            query = ("SELECT COUNT(1) as cnt FROM dbo.idmrunlog "
                     "WHERE CAST(IdmRunEndTimeUTC as DATE) = CAST(CURRENT_TIMESTAMP AS DATE)")
            print("STARTING QUERY EXECUTION")
            query_result = sql_server.execute_query(query=query)
            print("QUERY COMPLETED")
            if query_result.fetchone()["cnt"] == 1:
                print("AC available, calling my master to make something about it")
                notifier = Notifier()
                notifier.call()
                sleep(60 * 5)
            else:
                print("AC not available yet, waiting a little bit more")
                sleep(60 * 10)
        except Exception:
            print("The python code is broken, calling to check")
            notifier = Notifier()
            notifier.call()
            sleep(60 * 5)


if __name__ == "__main__":
    main()
