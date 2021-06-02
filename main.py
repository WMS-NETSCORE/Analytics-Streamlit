import warnings
import numpy as np
import pandas as pd
import streamlit as st
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Netscore Sales Data",page_icon=":random:",initial_sidebar_state='expanded')
st.title("Products Data")
# Read Data
df= pd.read_csv("https://raw.githubusercontent.com/WMS-NETSCORE/Analytics-Streamlit/main/AIDemandPlanningJYResults300.zip",compression='zip')
dfna=df.dropna(subset=['Class (no hierarchy)'])
df1=dfna.drop_duplicates(keep='last')
df1['Date Created']= pd.to_datetime(df1['Date Created'])
df1['year']=df1['Date Created'].dt.year
df1['month']=df1['Date Created'].apply(lambda x:x.strftime('%B'))
df1['month_num']=df1['Date Created'].dt.month
df1['day']=df1['Date Created'].apply(lambda x:x.strftime('%A'))
df1['quet']=df1['Date Created'].dt.quarter
df1['year']=df1['year'].astype(str)
df1['Color']=df1['Color'].astype(str)

df1.Pattern=df1.Pattern.str.split(";",expand=True)
print(df1.columns)
y=['2017','2018','2019','2020','2021']

col1,col2,col3=st.beta_columns(3)
with col1:
    yr=st.selectbox("Select year:",options=['2017','2018','2019','2020','2021'])

with col2:
    item=st.selectbox("Select Item:",options=df1['Class (no hierarchy)'].value_counts().index)
with col3:
    metric=st.selectbox("Select Item:",options=['Total Sales','Inventory'])

for j in y:
    if j in yr:
        for i in df1['Class (no hierarchy)'].value_counts().index:
            if i in item:
                if i == 'RUG':
                  if 'Total Sales' in metric:
                         data =pd.DataFrame(df1.loc[(df1['Class (no hierarchy)'] == i) & (df1['year'] == j), ['Pattern','Color','month','Item']].groupby(['month','Pattern','Color']).count())
                         rg = pd.pivot_table(index=['Pattern','Color'], columns=['month'], values='Item', aggfunc=np.sum,data=data, fill_value=0)
                         rg['total'] = rg.sum(axis=1)
                         st.table(rg)
                else:
                    data1 = pd.DataFrame(df1.loc[ (df1['Class (no hierarchy)'] == i) & (df1['year'] == j), ['Color', 'month', 'Item']].groupby(['month', 'Color']).count())
                    rg1 = pd.pivot_table(index=['Color'], columns=['month'], values='Item', aggfunc=np.sum, data=data1,fill_value=0)
                    rg1['total'] = rg1.sum(axis=1)
                    st.table(rg1)
