import pyodbc 
import pandas as pd
print(pyodbc.drivers())
# conn = pyodbc.connect(DRIVER= '{ODBC Driver 17 for SQL Server}',
#                     SERVER='15.206.42.4',
#                     DATABASE = 'DatabaseName',
#                     PORT=1433,
#                     Trusted_Connection = 'Yes',
#                     UID = 'sa',
#                     PWD = '1@B3ngal1',
#                     Authentication = 'ActiveDirectoryPassword'
#                     )
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=15.206.42.4;'
                      'UID=sa;'
                      'PWD=1@B3ngal1;')



cursor = conn.cursor()

print("success")
cursor = conn.cursor()
df=pd.read_sql_query("SELECT * FROM  [FactsetData].[dbo].[view_annual_xlrt_data] WHERE date >= '2019'", conn)

df.head(3)
#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+endpoint+';DATABASE='+database_name+';UID='+username+';PWD='+ password)
