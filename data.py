import sqlite3

import pandas as pd

con = sqlite3.connect("database.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("select * from tasks")
rows = cur.fetchall();
header_list=['Name','Age','Sex','cp','trestbps','chol','fbs','restecg','thalach','exang','Oldpeak','ST_Slope','ca','thal' ]
data=pd.DataFrame(rows,columns=header_list)
print(data)