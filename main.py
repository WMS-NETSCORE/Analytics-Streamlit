import warnings
import numpy as np
import pandas as pd
import streamlit as st
import base64
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Netscore Sales Data",page_icon=":random:",initial_sidebar_state='expanded')
st.title("Products Data")
# Read Data
df = pd.read_csv("https://4809897.app.netsuite.com/core/media/media.nl?id=7472655&c=4809897&h=Pve73pI_qvxpMNEfP9MAmhvo5-PlX4301Yy5Jr1Bw7t6BmKq&_xt=.csv",sep=',')
dfna=df.dropna(subset=['Class (no hierarchy)'])
df1=dfna.drop_duplicates(keep='last')
df1.Pattern=df1.Pattern.str.split(";",expand=True).get(0)
df1['Date Created']= pd.to_datetime(df1['Date Created'])
df1['year']=df1['Date Created'].dt.year
df1['month']=df1['Date Created'].apply(lambda x:x.strftime('%B'))
df1['month_num']=df1['Date Created'].dt.month
df1['day']=df1['Date Created'].apply(lambda x:x.strftime('%A'))
df1['quet']=df1['Date Created'].dt.quarter
df1['year']=df1['year'].astype(str)
df1['Color']=df1['Color'].astype(str)
y=['2017','2018','2019','2020','2021']

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.
    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.
    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')
    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'





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
                          if st.button('Download Dataframe as CSV'):
                              tmp_download_link = download_link(rg, 'Rugs_Report.csv', 'Click here to download your data!')
                              st.markdown(tmp_download_link, unsafe_allow_html=True)
                                
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






