import streamlit as st
import numpy as np
import time
import pandas as pd
import re
import os
import matplotlib.pyplot as plt

import seaborn as sns
import subprocess
import altair as alt
import datetime

current_date = datetime.date.today()

date=current_date.strftime("%Y-%m-%d")
file_path = "/var/www/data/logs/2023/datasource_log.txt"
st.markdown("<style>h1{color: green;}</style>", unsafe_allow_html=True)

st.title("VinQuery Dashboard")
Year = st.sidebar.selectbox('Select Year**',[2023])
Month = None
Day = None
if st.sidebar.checkbox("Choose Month[Optional]"):
   Month = st.sidebar.selectbox("Select a Month",["None"] + [f"{x:02}" for x in range(1, 13)])
   if Month != "None":
      if st.sidebar.checkbox("Choose Day[Optional]"):
         Day = st.sidebar.selectbox("Select a day", ["None"] + [f"{x:02}" for x in range(1, 32)])
         st.sidebar.write(f"You have selected  {Day} day" )
if(st.sidebar.button('Submit')):
    date = f"{Year}-{Month}-{Day}"
    date = date.replace("-None", "")
    st.success("You have selected " +date)
    if len(date) == 4 :
     file_path = file_path
    else :
     dest_file_path = f"/root/dashboard/{date}.txt"
     if os.path.exists(dest_file_path):
         os.remove(dest_file_path)
     command = f'cat "{file_path}"  | grep "{date}" >> {dest_file_path}'
     #st.warning(command)
     subprocess.check_output(command, shell=True).decode('utf-8').strip()
     file_path = dest_file_path

    def get_success_count(file_path,source) :
      try:
        #command = f'cat "{file_path}" | grep "::200" | wc -l'
        if source == 'ac' :
           command = f"awk '/::ac::/ && /::200::We found/  {{count += 1}} END {{print count}}'  {file_path} "
        else :
           command = f"awk '/::cf::/ && /::200::/  {{count += 1}} END {{print count}}'  {file_path} "
        result = subprocess.check_output(command, shell=True).decode('utf-8').strip()
        count = int(result)
        print("Number of lines with '::200' match:", count)
        return count
      except subprocess.CalledProcessError as e:
        print("Error executing the command:", e)

    def get_total_count(file_path,source) :
      try:
        #command = f'cat "{file_path}"  | wc -l'

        command =    f"awk '/::{source}::/ {{count += 1}} END {{print count}}'  {file_path} "
        result = subprocess.check_output(command, shell=True).decode('utf-8').strip()
        count = int(result)
        print("Number of lines in file ", count)
        return count
      except subprocess.CalledProcessError as e:
        print("Error executing the command:", e)


    try :
      ac_success_count = get_success_count(file_path,'ac')
    except :
      ac_success_count = 0
    try :
      ac_total_count = get_total_count(file_path,'ac')
    except :
      ac_total_count = 0

    #plot = alt.Chart(df_counts).mark_bar().encode(
     #  x='TimeStamp',
      # y='Count',
       #color=alt.Color('Status', scale=alt.Scale(range=['blue', 'orange'])),
       #column='Status',
       #tooltip=['TimeStamp', 'Count']
       #).properties(
       #width=200,
       #height=300
     #)
    y = np.array([ac_success_count,ac_total_count - ac_success_count])
    mylabels = ['AC_Success_count','AC_Failure_count']
    chart = plt.pie(y, labels=mylabels, autopct='%1.1f%%')
    plt.legend()
    plt.title("AC Datasource")
    st.info(f"Success Count for AC : {ac_success_count}")
    st.error(f"Failure Count for AC : {ac_total_count - ac_success_count}")

    for text in chart[2]:
        text.set_fontsize(12)
    fig = plt.gcf()

    st.pyplot(fig)
    plt.clf()

    #st.altair_chart(plot)

    try :
      cf_success_count = get_success_count(file_path,'cf')
    except :
      cf_success_count = 0
    try :
      cf_total_count = get_total_count(file_path,'cf')
    except :
      cf_total_count = 0

    y1 = np.array([cf_success_count,cf_total_count - cf_success_count])
    mylabel = ['CF_Success_count','CF_Failure_count']
    chart1 = plt.pie(y1, labels=mylabel, autopct='%1.1f%%')
    plt.legend()
    plt.title("CF Datasource")
    st.info(f"Success Count for CF : {cf_success_count}")
    st.error(f"Failure Count for CF : {cf_total_count - cf_success_count}")

    for text in chart1[2]:
        text.set_fontsize(12)
    fig1 = plt.gcf()

    st.pyplot(fig1)






