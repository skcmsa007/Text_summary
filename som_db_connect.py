from urllib import parse
from sqlalchemy import create_engine

connecting_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:15.206.42.4.database.windows.net,1433;Database=<your database name>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated'
params = parse.quote_plus(connecting_string)

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
connection = engine.connect()
result = connection.execute("select 1+1 as res")
for row in result:
    print("res:", row['res'])
connection.close()