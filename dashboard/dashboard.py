import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
all_data = pd.read_csv('all_data.csv')

def select_district(data):
    districts = data['station'].unique()
    selected_district = st.sidebar.selectbox('Select a district', districts)
    return selected_district

def filter_data(data, district, start_date, end_date):
    filtered_data = data[data['station'] == district]
    filtered_data = filtered_data[(pd.to_datetime(filtered_data['datetime']) >= start_date) & (pd.to_datetime(filtered_data['datetime']) <= end_date)]
    return filtered_data

def display_average_climate(filtered_data, selected_district):
    avg_temp = filtered_data['TEMP'].mean()
    avg_pres = filtered_data['PRES'].mean()
    avg_dewp = filtered_data['DEWP'].mean()
    avg_rain = filtered_data['RAIN'].mean()
    st.write(f'### Average Climate Data for {selected_district}')
    avg_climate_dict = {'TEMP': avg_temp, 'PRES': avg_pres, 'DEWP': avg_dewp, 'RAIN': avg_rain}
    avg_climate_df = pd.DataFrame.from_dict(avg_climate_dict, orient='index', columns=['Average'])
    st.table(avg_climate_df)

def display_average_pm(filtered_data, selected_district):
    avg_pm25 = filtered_data['PM2.5'].mean()
    avg_pm10 = filtered_data['PM10'].mean()
    st.write(f'### Average PM2.5 and PM10 for {selected_district}')
    avg_pm_dict = {'PM2.5': avg_pm25, 'PM10': avg_pm10}
    avg_df = pd.DataFrame.from_dict(avg_pm_dict, orient='index', columns=['Average'])
    st.bar_chart(avg_df)

def display_monthly_trend_line(filtered_data, selected_district):
    trend_data = filtered_data[['datetime', 'SO2', 'NO2', 'O3']]
    trend_data['datetime'] = pd.to_datetime(trend_data['datetime'])
    trend_data.set_index('datetime', inplace=True)
    monthly_trend = trend_data.resample('M').mean() 
    st.write(f'### Monthly Trend for SO2, NO2, and O3 in {selected_district}')
    st.line_chart(monthly_trend[['SO2', 'O3', 'NO2']])

def display_monthly_trend_co(filtered_data, selected_district):
    trend_data = filtered_data[['datetime', 'CO']]
    trend_data['datetime'] = pd.to_datetime(trend_data['datetime'])
    trend_data.set_index('datetime', inplace=True)
    monthly_trend = trend_data.resample('M').mean()
    st.write(f'### Monthly Trend for CO in {selected_district}')
    st.line_chart(monthly_trend['CO'])

def main():
    selected_district = select_district(all_data)
    start_date = pd.Timestamp(st.sidebar.date_input("Start Date"))
    end_date = pd.Timestamp(st.sidebar.date_input("End Date"))
    filtered_data = filter_data(all_data, selected_district, start_date, end_date)
    display_average_climate(filtered_data, selected_district)
    display_average_pm(filtered_data, selected_district)
    display_monthly_trend_line(filtered_data, selected_district)
    display_monthly_trend_co(filtered_data, selected_district)

if __name__ == '__main__':
    st.title('Air Quality Dashboard')
    st.write('Visualize Average Climate Data, Average PM2.5 and PM10, and Monthly Trend for SO2, NO2, O3, and CO')
    main()