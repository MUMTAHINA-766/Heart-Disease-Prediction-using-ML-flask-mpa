import imp
from flask import Flask, render_template, request
import pickle
import pandas as pd
import sqlite3 as sql
####
import matplotlib.pyplot as plt
import pickle
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Scatter, Pie
from pyecharts.commons.utils import JsCode

###
conn = sql.connect('database.db')
print("Opened database successfully") ;

# conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
#                                     Name text,
#                                     Age real,
#                                     Sex real,
#                                     cp real,
#                                     trestbps real,
#                                     chol real,
#                                     fbs real,
#                                     restecg real,
#                                     thalach real,
#                                     exang real,
#                                     Oldpeak real,
#                                     ST_Slope real,
#                                     ca real,
# 				                    thal real
#                                 );""")
#
#
#
# print ("Table created successfully");
# conn.close()


app = Flask(__name__)

"""Show graph and piecharts"""
######################bar chart#############################

list_age = []
list_sex = []
list_cp = []
list_trestbps = []
list_chol = []
list_fbs = []
list_restecg = []
list_thalach = []
list_exang = []
list_oldpeak = []
list_slope = []
list_ca = []
list_thal = []
list_target = []


def loadDataFromDataBase():
    list_age.clear()
    list_sex.clear()
    list_cp.clear()
    list_trestbps.clear()
    list_chol.clear()
    list_fbs.clear()
    list_restecg.clear()
    list_thalach.clear()
    list_exang.clear()
    list_oldpeak.clear()
    list_slope.clear()
    list_ca.clear()
    list_thal.clear()
    list_target.clear()

    con = sql.connect("heart.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from heart")

    rows = cur.fetchall()

    for row in rows:
        list_age.append(row[0])
        list_sex.append(row[1])
        list_cp.append(row[2])
        list_trestbps.append(row[3])
        list_chol.append(row[4])
        list_fbs.append(row[5])
        list_restecg.append(row[6])
        list_thalach.append(row[7])
        list_exang.append(row[8])
        list_oldpeak.append(row[9])
        list_slope.append(row[10])
        list_ca.append(row[11])
        list_thal.append(row[12])
        list_target.append(row[13])

def bar_base_stack():
    c = (
        Bar()
            # Add X-axis data
            .add_xaxis(list_target)

            .add_yaxis("age", list_age, stack="stack1")
            .add_yaxis("sex", list_sex, stack="stack1")
            .add_yaxis("cp", list_cp, stack="stack1")
            .add_yaxis("trestbps", list_trestbps, stack="stack1")
            .add_yaxis("chol", list_chol, stack="stack1")
            .add_yaxis("fbs", list_fbs, stack="stack1")
            .add_yaxis("restecg", list_restecg, stack="stack1")
            .add_yaxis("thalach", list_thalach, stack="stack1")
            .add_yaxis("exang", list_exang, stack="stack1")
            .add_yaxis("oldpick", list_oldpeak, stack="stack1")
            .add_yaxis("slope", list_slope, stack="stack1")
            .add_yaxis("ca", list_ca, stack="stack1")
            .add_yaxis("thal", list_thal, stack="stack1")
            

            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
           
        
    )
    return c

###################pie chart


############# show chart function

@app.route("/barStackChart")
def get_bar_stack_chart():
    #Read the data to be displayed from the database
    loadDataFromDataBase()
    # Get stacked bar objects
    c = bar_base_stack()
    #Return the stacked bar object to the front-end page for display
    return c.dump_options_with_quotes()
########################3
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/showData')
def table():
    
    # converting csv to html
    data = pd.read_csv('models/heart.csv')
    return render_template('showData.html', tables=[data.to_html()], titles=[''])

@app.route('/original')
def original():
    return render_template('original.html')

@app.route("/graph", methods=['GET', 'POST'])
def graphChart():
    return render_template('graph.html')

@app.route("/matrix", methods=['GET', 'POST'])
def confusionMatrix():
    return render_template('matrix.html')


@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        fname = str(request.form['fname'])
        age = float(request.form['age'])
        sex = float(request.form['sex'])
        cp = float(request.form['cp'])
        trestbps = float(request.form['trestbps'])
        chol = float(request.form['chol'])
        fbs= float(request.form['fbs'])
        restecg = float(request.form['restecg'])
        thalach = float(request.form['thalach'])
        exang = float(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        ca = float(request.form['ca'])
        thal = float(request.form['thal'])
        # con = sqlite3.connect("database.db")
        # cur = con.cursor()
        # cur.execute(
        #     "INSERT INTO tasks (Name,Age,Sex,cp,trestbps,chol,fbs,restecg,thalach,exang,Oldpeak,ST_Slope,ca,thal )VALUES(?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?)",
        #     (fname, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal))
        #
        # con.commit()
        # print("Record successfully added")

        pred_args = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        files = ['Decision_Tree (2).pkl', 'random_forest (1).pkl', 'knn.pkl', 'Naive_Bayes.pkl']
        res=[]
        for model_file in files:

            mul_reg = open(model_file, 'rb')
            ml_model = pickle.load(mul_reg)
            model_predcition = ml_model.predict([pred_args])
            if model_predcition == 1:
                res = 'Affected'
            else:
                res = 'Not affected'


        #return res
    return render_template('predict.html', prediction = res, fname = fname, age = age, sex = sex, cp = cp, trestbps = trestbps, chol = chol, fbs = fbs, restecg = restecg, thalach =thalach, exang = exang, oldpeak = oldpeak, slope =slope, ca = ca, thal = thal )





if __name__ == '__main__':
    app.run()
