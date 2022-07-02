import sqlite3 as sql
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
import  pandas as pd
from pyecharts.faker import Faker

def create_database():
    conn = sql.connect('heart.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE sample( age TEXT,sex TEXT,cp TEXT,trestbps TEXT,chol TEXT,fbs TEXT,restecg TEXT,thalach TEXT,exang TEXT,oldpeak TEXT,slope TEXT,ca TEXT,thal TEXT,target TEXT)')
    print("Table created successfully")
    conn.close()


def save_data():
    df = pd.read_csv("models/heart.csv")
    try:
        with sql.connect("heart.db") as con:
            cur = con.cursor()
            for i in df.index:
                cur.execute("INSERT INTO sample (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (df["age"][i],df["sex"][i],df["cp"][i],df["trestbps"][i],df["chol"][i],df["fbs"][i],df["restecg"][i],df["thalach"][i],df["exang"][i],df["oldpeak"][i],df["slope"][i],df["ca"][i],df["thal"][i],df["target"][i]))
            con.commit()
            print("All data successfully added")
    except:
        print("error in insert operation")
    finally:
        con.close()
    return


if __name__ == '__main__':
    create_database()
    save_data()