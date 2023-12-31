import os

from sql_server import SQLServerDatabase
from notifier import Notifier


def main():
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
        if query_result["cnt"] == 1:
            print("AC available, calling my master to make something about it")
            notifier = Notifier()
            notifier.call()
        else:
            print("AC not available yet, waiting a little bit more")
    except Exception:
        print("The python code is broken, calling to check")
        notifier = Notifier()
        notifier.call()


if __name__ == "__main__":
    main()
