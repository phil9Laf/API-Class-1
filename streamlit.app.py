import streamlit as st
from datetime import datetime
import gspread

credentials_info = st.secrets['gcp_service_account']

gc = gspread.service_account_from_dict(credentials_info)

spreadsheet_id = "1Ez11ZdK8UKWFitEM2iZmY3kL8wtsZilEJI3-PNLI1Z4"
sheet = gc.open_by_key(spreadsheet_id).sheet1

st.title('Green Boot Camp')
st.subheader('Attendance')

date = st.date_input('Date')

people_option = ['Marie', 'Jacky', 'Satish', 'Aycan',
                'Lukas', 'Andreas', 'Zhara', 'Moritz', 'Phil', 'Niko']
people = st.selectbox('Select the Person', people_option)

Attendance_option = ['Present', 'Absent']
attendance = st.selectbox('Attendance', Attendance_option)

if st.button('Submit'):
    headers = ['Date', 'Person', 'Attendance']  
    dataToappend = [date.strftime('%Y-%m-%d'), people, attendance]  
    next_row = len(sheet.get_all_values()) + 1
    
    if next_row == 2:
        sheet.insert_row(headers, next_row - 1)
    
    existing_entries = sheet.col_values(1)  
    existing_dates_people = [(row[0], row[1]) for row in sheet.get_all_values()[1:]]

    if (date.strftime('%Y-%m-%d'), people) in existing_dates_people:
        st.warning("Attendance for this person on this date already exists.")
    else:
        sheet.insert_row(dataToappend, next_row, value_input_option='USER_ENTERED')
        st.success('Attendance has been recorded')
