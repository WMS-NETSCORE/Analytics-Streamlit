import warnings
import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Netscore Sales Data",page_icon=":random:",initial_sidebar_state='expanded')
st.title("Products Data")
# Read Data
df = pd.read_csv("https://4809897.app.netsuite.com/core/media/media.nl?id=7472655&c=4809897&h=Pve73pI_qvxpMNEfP9MAmhvo5-PlX4301Yy5Jr1Bw7t6BmKq&_xt=.csv",sep=',')
dfna=df.dropna(subset=['Class (no hierarchy)'])
df1=dfna.drop_duplicates(keep='last')
df1.rename(columns = {'Rug Pattern':'Pattern'}, inplace = True)
df1['Date Created']= pd.to_datetime(df1['Date Created'])
df1['year']=df1['Date Created'].dt.year
df1['month']=df1['Date Created'].apply(lambda x:x.strftime('%B'))
df1['month_num']=df1['Date Created'].dt.month
df1['day']=df1['Date Created'].apply(lambda x:x.strftime('%A'))
df1['quet']=df1['Date Created'].dt.quarter
df1['year']=df1['year'].astype(str)
df1['Color']=df1['Color'].astype(str)
y=['2017','2018','2019','2020','2021']
df1.Pattern=df1.Pattern.str.split(";",expand=True)
print(df1.columns)


s = st.selectbox("Reports As of Today",("Select Options","By Item", "Top 10 Shipping Cities"))
if st.checkbox("Report As of Today"):
    if 'By Item' in s:
        st.table(df1['Class (no hierarchy)'].value_counts())
    elif 'Top 10 Shipping Cities' in s:
        st.table(df1['Shipping City'].value_counts().head(10))
    else:
        st.write('')


col1,col2,col3=st.beta_columns(3)
with col1:
    yr=st.selectbox("Select year:",options=['2017','2018','2019','2020','2021'])
with col2:
    item=st.selectbox("Select Item:",options=df1['Class (no hierarchy)'].value_counts().index)
with col3:
    metric=st.selectbox("Select Metric:",options=['Total Items Sold','Shipping City','Top 10 Stores'])

if st.checkbox("Show/Hide"):
    for j in y:
        if j in yr:
            for i in df1['Class (no hierarchy)'].value_counts().index:
                if i in item:
                    if i == 'RUG':
                      if 'Total Items Sold' in metric:
                          data = pd.DataFrame(df1.loc[(df1['Class (no hierarchy)'] == i) & (df1['year'] == j), ['Pattern','Color','month_num','Item']].groupby(['month_num','Pattern','Color']).count())
                          rg = pd.pivot_table(index=['Pattern','Color'], columns=['month_num'], values='Item', aggfunc=np.sum,data=data, fill_value=0)
                          rg['total'] = rg.sum(axis=1)
                          st.write("Displaying Data of ",i,"Pattren with Color")
                          st.table(rg)
                      elif 'Shipping City' in metric:
                          sc=df1.loc[(df1['Class (no hierarchy)'] == i) & (df1['year'] == j),['Shipping City']].value_counts().head(10)
                          st.table(sc)
                      else:
                          c = df1.loc[(df1['Class (no hierarchy)'] == i) & (df1['year'] == j), ['Company Name']].value_counts().head(10)
                          st.table(c)
                    else:
                      if 'Total Items Sold' in metric:
                          data1 = pd.DataFrame(df1.loc[ (df1['Class (no hierarchy)'] == i) & (df1['year'] == j), ['Color', 'month_num', 'Item']].groupby(['month_num', 'Color']).count())
                          rg1 = pd.pivot_table(index=['Color'], columns=['month_num'], values='Item', aggfunc=np.sum, data=data1,fill_value=0)
                          rg1['total'] = rg1.sum(axis=1)
                          st.write("Displaying Data of ",i,"with Color")
                          st.table(rg1)
                      elif 'Shipping City' in metric:
                          sc1 = df1.loc[(df1['Class (no hierarchy)'] == i) & (df1['year'] == j), ['Shipping City']].value_counts().head(10)
                          st.table(sc1)
                      else:
                          c1 = df1.loc[(df1['Class (no hierarchy)'] == i) & (df1['year'] == j), ['Company Name']].value_counts().head(10)
                          st.table(c1)






