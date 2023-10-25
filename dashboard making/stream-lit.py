import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="Dashboard-climate",page_icon="🌍",layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#open file csv
df = pd.read_csv('https://raw.githubusercontent.com/putriafia26/dashboard-climate/master/climate-change-clean.csv', parse_dates = ['date'])

#change datetime on dataframe to compare native date on python
df['date']=pd.to_datetime(df['date']).dt.date

#input date range
st.sidebar.subheader('Date range')
min_date = df['date'].min()
max_date = df['date'].max()
start_date, end_date = st.sidebar.date_input(label = 'Date range',
                                             min_value=min_date,
                                             max_value=max_date,
                                             value=[min_date, max_date])


#filter by province
st.sidebar.subheader('Province')
provinces = ["All province"] + list(df['province_name'].value_counts().keys().sort_values())
province = st.sidebar.selectbox(
                "Select province",
                options=provinces
)

#filter by station
st.sidebar.subheader('Station')
stations = ["All station"] + list(df['station_name'].value_counts().keys().sort_values())
station = st.sidebar.selectbox(
                "Select station",
                options=stations
)

st.sidebar.markdown('''
---
Get the original data here: [Data Source](https://www.kaggle.com/datasets/greegtitan/indonesia-climate?select=station_detail.csv).
''')

# apply filter
outputs = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
if province != "All province":
    outputs = outputs[outputs['province_name'] == province]
if station != "All station":
    outputs = outputs[outputs['station_name'] == station]

st.header("Climate Change in Indonesia (2010-2020)")
st.caption("By : Putri Afia Nur Fallahi")

# metrics
st.markdown('#### Metrics')
avg_temperature=outputs['Tavg'].mean()
avg_rh=outputs['RH_avg'].mean()
avg_rr=outputs['RR'].mean()
avg_ss=outputs['ss'].mean()

col1, col2, col3, col4=st.columns(4)
with col1:
    st.info('Average Temperature', icon='📌')
    st.metric(label="avg temperature", value=str(f"{avg_temperature:,.2f}")+"°C")
with col2:
    st.info('Average Humidity', icon='📌')
    st.metric(label="avg humidity", value=str(f"{avg_rh:,.2f}")+"%")
with col3:
    st.info('Average rainfall', icon='📌')
    st.metric(label="avg rainfall", value=str(f"{avg_rr:,.2f}")+" mm")
with col4:
    st.info('Average Sun Duration', icon='📌')
    st.metric(label="avg sun", value=str(f"{avg_ss:,.2f}")+" hour")

#monthly avg temp
st.markdown('#### Average Temperature Change by Period')
temp_period=outputs.groupby(by=pd.to_datetime(outputs['date']).dt.month)['Tavg'].mean()
fig_temp=px.line(
    temp_period, 
    x=temp_period.index,
    y="Tavg",
    orientation="v",
    title="<b> Monthly Avg Temperature Change <b>",
    color_discrete_sequence=["#0083b8"]*len(temp_period),
    template="plotly_white",
)
fig_temp.update_layout(
    xaxis=dict(tickmode="linear"),
    yaxis=(dict(showgrid=False))
)

#annual avg temperature
temp_year=outputs.groupby(by=pd.to_datetime(outputs['date']).dt.year)['Tavg'].mean()
fig_year=px.line(
    temp_year, 
    x=temp_year.index,
    y="Tavg",
    orientation="v",
    title="<b> Annual Avg Temperature Change <b>",
    color_discrete_sequence=["#0083b8"]*len(temp_year),
    template="plotly_white",
)
fig_year.update_layout(
    xaxis=dict(tickmode="linear"),
    yaxis=(dict(showgrid=False))
)
left,right=st.columns(2)
left.plotly_chart(fig_temp, use_container_width=True)
right.plotly_chart(fig_year, use_container_width=True)

# top 10 province with highest avg temperature
most_temp = outputs.groupby(['province_name'])['Tavg'].mean().nlargest(10).sort_values()
most_prov = px.bar(
    most_temp,
    orientation="h",
    title="<b> Top 10 Province with the Highest Avg Temperature <b>",  
    color=most_temp,
)
most_prov.update_layout(
    xaxis=dict(tickmode="linear"),
    yaxis=(dict(showgrid=False))
)

# top 10 province with lowest avg temp
low_temp = outputs.groupby(['province_name'])['Tavg'].mean().nsmallest(10)
east_prov = px.bar(
    low_temp,
    orientation="h",
    title="<b> Top 10 Province with the Lowest Avg Temperature <b>",  
    color=low_temp,
)
east_prov.update_layout(
    xaxis=dict(tickmode="linear"),
    yaxis=(dict(showgrid=False)),
)
left,right=st.columns(2)
left.plotly_chart(most_prov, use_container_width=True)
right.plotly_chart(east_prov, use_container_width=True)

#monthly avg rain
st.markdown('#### Average Rain Change by Period')
rain_month=outputs.groupby(by=pd.to_datetime(outputs['date']).dt.month)['RR'].mean()
fig_rain_month=px.bar(
    rain_month, 
    x=rain_month.index,
    y="RR",
    orientation="v",
    title="<b> Monthly Avg Rain Change <b>",
    color=rain_month,
    template="plotly_white",
)
fig_rain_month.update_layout(
    xaxis=dict(tickmode="linear"),
    yaxis=(dict(showgrid=False))
)

#annual avg rain
rain_year=outputs.groupby(by=pd.to_datetime(outputs['date']).dt.year)['RR'].mean()
fig_rain_year=px.line(
    rain_year, 
    x=temp_year.index,
    y="RR",
    orientation="v",
    title="<b> Annual Avg rain Change <b>",
    color_discrete_sequence=["#0083b8"]*len(rain_year),
    template="plotly_white",
)
fig_rain_year.update_layout(
    xaxis=dict(tickmode="linear"),
    yaxis=(dict(showgrid=False))
)
left,right=st.columns(2)
left.plotly_chart(fig_rain_month, use_container_width=True)
right.plotly_chart(fig_rain_year, use_container_width=True)

#min max temp
st.markdown('#### Min Max temperature')
min_temp = outputs.groupby(['date'])['Tn'].mean()
max_temp = outputs.groupby(['date'])['Tx'].mean()

fig_min_temp=px.scatter(
    min_temp, 
    y="Tn",
    title="<b> Min Temperature <b>",
    color_discrete_sequence=["#8A8AFF"]*len(min_temp),
    template="plotly_white",
)
fig_min_temp.update_layout(
    yaxis=(dict(showgrid=False))
)

fig_max_temp=px.scatter(
    max_temp, 
    y="Tx",
    title="<b> Max Temperature <b>",
    color_discrete_sequence=["#FFA500"]*len(max_temp),
    template="plotly_white",
)
fig_max_temp.update_layout(
    yaxis=(dict(showgrid=False))
)

left,right=st.columns(2)
left.plotly_chart(fig_min_temp, use_container_width=True)
right.plotly_chart(fig_max_temp, use_container_width=True)


