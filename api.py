# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request,render_template
import requests
import pandas as pd
from datetime import datetime as dt,timezone,timedelta
import pytz
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
import csv
from flask_apscheduler import APScheduler


# creating a Flask app
app = Flask(__name__) 



scheduler = APScheduler()
#scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


def fetch_api_info_github():
     response = requests.get("https://api.github.com/events", params={"per_page": 100})  
     data = response.json()

     return data




@scheduler.task('interval', id='do_job_1',minutes=10)
def extract_data_write_to_csv():
    data = fetch_api_info_github()
    type_of = []
    name = []
    date_created = []
    
    required_types = ["WatchEvent", "PullRequestEvent", "IssuesEvent"]
    for elements in data:
        for i in required_types:
            if elements["type"] == i in required_types:
                type_of.append(elements["type"])
                name.append(elements["repo"]["name"])
                date_created.append(elements["created_at"])
   
    fields = ["type", "name", "data_created"]

    # data rows of csv file
    rows = [type_of, name, date_created]

    # name of csv file
    filename = "github_data.csv"

    # This appends new data to csv
    with open(filename, "a") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields

        # writing the data rows
        # csvwriter.writerows(rows)
        for i in range(0, len(type_of)):
            csvwriter.writerow([type_of[i], name[i], date_created[i]])
    


    
@app.route('/', methods = ['GET'])
def total_event_groupby():
    df = pd.read_csv('github_data.csv')
    df['date_created'] =  pd.to_datetime(df['date_created'],utc=True)
    #print(df['date_created'][0])
    df['date_created'] =  df[(df['date_created'])>=(dt.now(tz=pytz.UTC)- timedelta(minutes=10))]['date_created'] #hours = 6,12, 24
    # this groups types and counts with the date based on the return time
    df_2 = df.groupby(['type'])['date_created'].count().reset_index()
    type_list =df_2.type.tolist()
    number_of_occurence_in_10mins_offset =df_2.date_created.tolist()
    new_dic=dict(zip(type_list,number_of_occurence_in_10mins_offset))
    return jsonify({'  types_count':  new_dic})

     


@app.route('/avg',methods = ['GET'])
def average_time():
   df = pd.read_csv('github_data.csv')
   df['date_created'] =  pd.to_datetime(df['date_created'],format="%Y-%m-%dT%H:%M:%SZ")
   avg_time =[]
   df_1 =df.loc[df['type']=='PullRequestEvent']# filtered all pull request
   #print(me)
   df_2 = df_1.groupby('name', as_index=False)['date_created'].mean() #getting average time by grouping by name
   name_list = df_2['name'].tolist() # converts name column to list
   time_list =df_2['date_created'].dt.time # extracting time only from datetime
   for i in time_list:
       avg_time.append(str(i))# converts time to string
   
         
   average_time_per_repo_name=dict(zip(name_list,avg_time))# zipping name and average to dictionary
          
   print(average_time_per_repo_name)
        

   
   return jsonify({'average_time_per_repo_name':  average_time_per_repo_name})








@app.route('/chart', methods = ['GET'])
def chart():
  df = pd.read_csv('github_data.csv')
  df['date_created'] =  pd.to_datetime(df['date_created'],utc=True)
  df_2 = df.groupby(['type'])['date_created'].count().reset_index()
  type_list =df_2.type.tolist()
  date_created_tolist=df_2.date_created.tolist()
  new_dic=dict(zip(type_list,date_created_tolist))
  labels =['IssuesEvent','PullRequestEvent','WatchEvent']
  data  =[new_dic['IssuesEvent'],new_dic['PullRequestEvent'],new_dic['WatchEvent']]
  return render_template(template_name_or_list='chart.html',data=data,labels=labels,)
 
if __name__ == '__main__':
    
    app.run(debug = True)