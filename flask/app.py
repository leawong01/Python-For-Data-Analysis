from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd
import random
import numpy as np



columns = ['likes', 'checkins', 'returns', 'category',
           'commBef min', 'commBef max', 'commBef avg', 'commBef med', 'commBef std',
           'comm24 min', 'comm24 max', 'comm24 avg', 'comm24 med', 'comm24 std',
           'comm48 min', 'comm48 max', 'comm48 avg', 'comm48 med', 'comm48 std',
           'comm24Bef min', 'comm24Bef max', 'comm24Bef avg', 'comm24Bef med', 'comm24Bef std',
           'diff2448 min', 'diff2448 max', 'diff2448 avg', 'diff2448 med', 'diff2448 std',
           'commBef', 'comm24', 'comm48', 'comm24Bef', 'diff2448', 'baseTime',
           'length', 'shares','promoted', 'hrs',
           'sun_pub', 'mon_pub', 'tue_pub', 'wed_pub', 'thu_pub', 'fri_pub','sat_pub', 
           'sun_base', 'mon_base', 'tue_base', 'wed_base', 'thu_base','fri_base', 'sat_base', 
           'output']

test_df = pd.read_csv("./Features_TestSet.csv", names = columns)

test_df.drop(labels=['checkins','comm24 min','comm24Bef min','comm48','comm48 min','commBef min','diff2448 med','length','likes','returns','shares', 'output'], axis=1, inplace=True)


app = Flask(__name__)

# render default webpage
@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

# when the post method detect, then redirect to success function
#@app.route('/', methods=['POST', 'GET'])
#def get_data():
#    if request.method == 'POST':
#        user = request.form['search']
#        return redirect(url_for('success', name=user))

@app.route('/predict', methods=['POST', 'GET'])
def get_prediction():
    index = random.randint(0,len(test_df))
    print(test_df.iloc[index,:])
    col = test_df.iloc[index,0:28]
    week_pub = test_df.iloc[index,28:35]
    week_base = test_df.iloc[index,35:42]
    for i in range(7):
        if week_pub[i] == 1:
            col['week_pub']= int(i+1)
        if week_base[i] == 1:
            col['week_base'] = int(i+1)

    return render_template('predict.html', list=col)

@app.route('/results', methods=['POST', 'GET'])
def get_result():
    req=request.form
    list_features = [x for x in req.values()]
    week_day = [float(x)-1 for x in list_features[-2:]]
    int_features = [float(x) for x in list_features[1:-2]]
    week_pub = np.zeros(7)
    week_pub[int(week_day[0])] = 1
    week_base = np.zeros(7)
    week_base[int(week_day[1])] = 1
    int_features.extend(week_pub)
    int_features.extend(week_base)
    final_features = [np.array(int_features)]

    if req['submit_button'] == 'RegLinear':
        model = pickle.load(open('./models/RegLinear.sav', 'rb'))
        name='Linear Regression'
        prediction = model.predict(final_features)
        output = round(prediction[0], 2) 
        print(output)

    if req['submit_button'] == 'RandomForest':
        model = pickle.load(open('./models/RandomForest.sav', 'rb'))
        name='Random Forest'
        prediction = model.predict(final_features)
        output = round(prediction[0], 2) 
        print(output)

    if req['submit_button'] == 'DecisionTree':
        model = pickle.load(open('./models/DecisionTree.sav', 'rb'))
        name='Decision Tree'
        prediction = model.predict(final_features)
        output = round(prediction[0], 2) 
        print(output)

    if req['submit_button'] == 'ElasticNet':
        model = pickle.load(open('./models/ElasticNet.sav', 'rb'))
        name='Elastic Net'
        prediction = model.predict(final_features)
        output = round(prediction[0], 2) 
        print(output)
    return render_template('results.html', model= name, output= output, list= list_features[1:])



