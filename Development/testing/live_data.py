import ast
import pandas as pd
import time as t

data = pd.read_csv("E:\Semester-2\DIVA\Project\Development\sample_data.csv")
data['module'] = data['file'].apply(lambda x : ast.literal_eval(x)['project'])
data['timestamp'] = pd.to_datetime(data.timestamp)  


start_time = pd.Timestamp('2019-02-25 00:12:00')
time = start_time
downloads = 0
packages = []
while True:
    old_time = time
    new_time = time + pd.Timedelta(seconds = 2)
    temp_data = data[(data['timestamp'] > old_time) & (data['timestamp'] <= new_time)]
    downloads += temp_data.shape[0]
    rate = temp_data.shape[0]/2
    packages.extend(list(set(temp_data['module'])))
    packages = list(set(packages))
    print('Unique Packages :', len(packages))
    print("Downloads : ", downloads)
    print("Rate : ", rate)
    time = new_time
    t.sleep(1)
    if temp_data.shape[0] == 0:
        break