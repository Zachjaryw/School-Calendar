import dropbox, json, io
import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st

def initialize():
  access = '8vYE9nXcBrIAAAAAAAAAASnG5cKRmMPdSMJiH-QximbXAXZR40C9EgmR1eZjYr9M'
  dbx = dropbox.Dropbox(access)
  dbx.users_get_current_account()
  return dbx

def toDBX(dbx, data,filename):
  with io.StringIO() as stream:
    json.dump(data, stream)
    #dbx.files_upload(stream.read().encode(), filename, mode=dropbox.files.WriteMode.overwrite)

def fromDBX(dbx, filename):
  _, res = dbx.files_download(filename)
  with io.BytesIO(res.content) as stream:
    data = json.load(stream)
  return data 

def setup_new_semester():
  global dbx
  global calendar
  global filename
  reset()
  toDBX(dbx, calendar, filename)

def save_cal():
  global calendar
  global dbx
  global filename
  toDBX(dbx, calendar, filename)

def reset():
  global calendar
  calendar = {
        'Assignment Name': [],
        'Assignment Due Date': [],
        'Class Code': [],
        'Assignment Notes': [],
        'Assignment Status': [],
        'Assignment Type': []
  }

def fromDateRange(lowDate, highDate):
  global calendar
  df = pd.DataFrame(calendar)
  df.sort_values('Assignment Due Date',inplace = True)
  df = df[df['Assignment Due Date'] >= lowDate][df['Assignment Due Date'] <= highDate]
  if df.empty == True:
    st.text(f'There are no assignments between {lowDate} and {highDate}.')
  else:
    st.dataframe(df)

def addAssignmentsFromFile(file):
  global calendar
  stuff = pd.read_excel(file)
  st.text(list(stuff.columns))
  if list(stuff.columns) == ['name','class_code','due_date','notes','status','ast_type']:
    name = stuff['name'].values.tolist()
    class_code = stuff['class_code'].values.tolist()
    due_date = stuff['due_date'].values.tolist()
    notes = stuff['notes'].values.tolist()
    status = stuff['status'].values.tolist()
    ast_type = stuff['ast_type'].values.tolist()
    for pos in range(len(name)):
      add(name[pos],class_code[pos],due_date[pos],notes[pos],status[pos],ast_type[pos])
    save_cal()
    st.text("All Files added.")
  else:
    st.text("File must have designated column names: ['name','class_code','due_date','notes','status','ast_type']")
    st.text('Please adjust file and try again.')


def add(name,class_code, due_date = str(dt.date.today()),notes = 'None',status = 'Incomplete', ast_type = 'Homework'):
  global calendar
  calendar['Assignment Name'] = list(calendar['Assignment Name']) + [str(name)]
  calendar['Assignment Due Date'] = list(calendar['Assignment Due Date']) + [str(due_date)]
  calendar['Class Code'] = list(calendar['Class Code']) + [str(class_code)]
  calendar['Assignment Notes'] = list(calendar['Assignment Notes']) + [str(notes)]
  calendar['Assignment Status'] = list(calendar['Assignment Status']) + [str(status)]
  calendar['Assignment Type'] = list(calendar['Assignment Type']) + [str(ast_type)]
  st.text(f'Assignment "{name}" added to 2021 Calendar')
  save_cal()

def show():
  global calendar
  df = pd.DataFrame(calendar)
  df.sort_values('Assignment Due Date',inplace = True)
  if df.empty == True:
    st.text('There are currently no assignments in the calendar')
  else:
    st.dataframe(df)
  
def thisWeek():
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  days_7 = str(dt.date.today() + dt.timedelta(weeks = 1))
  df = df[df['Assignment Due Date'] <= days_7]
  df = df[df['Assignment Status'] != 'Complete']
  if df.empty == True:
    st.text(f'There are no assignments due until after {days_7}')
  else:
    st.text('Assignments:\n')
    st.dataframe(df[df['Assignment Type'] != 'Reading'])
    st.text('\nReadings:\n')
    st.dataframe(df[df['Assignment Type'] == 'Reading'])
  
def shortThisWeek():
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  days_7 = str(dt.date.today() + dt.timedelta(weeks = 1))
  df = df[df['Assignment Due Date'] <= days_7]
  df = df[df['Assignment Status'] != 'Complete']
  if df.empty == True:
    st.text(f'There are no assignments due until after {days_7}')
  else:
    st.text('Assignments:\n')
    st.dataframe(df[df['Assignment Type'] != 'Reading'][['Assignment Name','Class Code','Assignment Due Date']])
    st.text('\nReadings:\n')
    st.dataframe(df[df['Assignment Type'] == 'Reading'][['Assignment Name','Class Code','Assignment Due Date']])

def thisMonth():
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  month = str(dt.date.today() + dt.timedelta(weeks = 4))
  df = df[df['Assignment Due Date'] <= month]
  df = df[df['Assignment Status'] != 'Complete']
  if df.empty == True:
    st.text(f'There are no assignments due until after {month}')
  else:
    st.dataframe(df)

def adjust(entry_pos, column, input):
  global calendar
  calendar[column][entry_pos] = input
  
  st.text(f'Assignment position {entry_pos} adjusted')
  thisWeek()
  save_cal()

def classCode(class_code):
  global calendar
  classes = {102:'Art',161:'Computer Science',315:'Business Finance',343:'Communications', 'DC':'DataCamp'}
  st.text(f'DataFrame Below is for {class_code}  {classes[class_code]}')
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  df = df[df['Class Code'] == str(class_code)]
  df = df[df['Assignment Status'] != 'Complete']
  if df.empty == True:
    st.text(f'There are no assignments for class code {class_code}')
  else:
    st.dataframe(df)
  
def previousAst():
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  df = df[df['Assignment Status'] == 'Complete']
  if df.empty == True:
    st.text(f'There are no complete assignments')
  else:
    st.dataframe(df)

def progress(index_pos, stage = 'Complete'):
  global calendar
  calendar['Assignment Status'][int(index_pos)] = str(stage)
  
  st.text(f"Assignment {str(calendar['Assignment Name'][int(index_pos)])} is now marked as {stage}")
  thisWeek()
  save_cal()

def byType(select_type):
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  df = df[df['Assignment Type'] == str(select_type)]
  df = df[df['Assignment Status'] != 'Complete']
  if df.empty == True:
    st.text(f'There are no assignments for assignment type {select_type}')
  else:
    st.dataframe(df)

def completeAction(Action):
  if Action == "Show Full Calendar":
    show()
  elif Action == "Progress":
    shortThisWeek()
    st.text("Input Assignment position (or positions seperated by commas)")
    index = st.text_input('Position Number')
    a = st.button('Submit')
    if a == True:
        if ',' in index:
          positions = index.split(',')
          for pos in positions:
            progress(int(pos))
        else:
          st.text("Input new state or leave empty to mark complete")
          state = str(st.text_input('Position Number'))
          b = st.button('Submit')
          if b == True:
              if state == "":
                progress(index)
              else:
                progress(index,state)
  elif Action == "Show Old Assignments":
    previousAst()
  elif Action == "Adjust Assignment":
    thisWeek()
    st.text("Input position of assignment to adjust")
    pos = int(st.number_input('Position number'))
    a = st.button('Select position')
    if a == True:
        st.text("Input the value for the column to adjust")
        for i in range(len(list(calendar.keys()))):
          st.text(f'{i}. {list(calendar.keys())[i]}')
        st.text('\n')
        col = int(st.text_input('Column to adjust'))
        while not(col >= 0 and col <= 5):
          st.text('Invalid input: please enter again')
        b = st.button('Select column')
        if b == True:
            st.text("Input adjusted value")
            new = st.text_input('New Value')
            c = st.button('Submit')
            if c == True:
                if col == 0: #'Assignment Name'
                  adjust(pos,'Assignment Name',new)
                elif col == 1:#'Assignment Due Date'
                  adjust(pos,'Assignment Due Date',new)
                elif col == 2:#'Class Code'
                  adjust(pos,'Class Code',new)
                elif col == 3:#'Assignment Notes'
                  adjust(pos,'Assignment Notes',new)
                elif col == 4:#'Assignment Status'
                  adjust(pos,'Assignment Status',new)
                elif col == 5:#'Assignment Type'
                  adjust(pos,'Assignment Type',new)
  elif Action == "Assignments Due This Week":
    thisWeek()
  elif Action == "Assignments Due This Month":
    thisMonth()
  elif Action == "New Assignment":
    st.text("New Assignment name")
    name = st.text_input('Assignment Name')
    a = st.button('Submit name')
    if a == True:
        st.text("Class Code")
        code = st.text_input('')
        b = st.button('Submit Class Code')
        if b == True:
            st.text('Due Date')
            date = st.text_input('')
            c = st.button('Submit Due Date')
            if c == True:
                st.text('Notes (leave empty for default)')
                notes = str(st.text_input(''))
                d = st.button('Submit Notes')
                if d == True:
                    st.text('Assignment Type (leave empty for default)')
                    type_ = str(st.text_input(''))
                    d = st.button('Submit Type')
                    if d == True:
                        if notes == "":
                          if type_ == "":
                            add(name,code,date)
                          else:
                            add(name,code,date,ast_type= type_)
                        else:
                          if type_ == "":
                            add(name,code,date,notes)
                          else:
                            add(name,code,date,notes,ast_type= type_)
  elif Action == "Show Assignments by Type":
    st.text('Enter assignment type')
    type_ = st.text_input('')
    if st.button('Submit'):
        byType(type_)
  elif Action == "Add Assignments from file":
    
    st.text('Please enter the file path here:')
    st.text("The file must have correct column names: ['name','class_code','due_date','notes','status','ast_type']")
    filePath = st.text_input('')
    if st.button('Submit'):
        addAssignmentsFromFile(filePath)
  elif Action == "Assignments In Date Range":
    st.text('Enter the first (lower) date:')
    lowDate = st.text_input('')
    if st.button('Submit date 1'):
        st.text('Enter the second (higher) date:')
        highDate = st.text_input('')
        if st.button('Submit date 2'):
            fromDateRange(lowDate,highDate)
  elif Action == "Review Single Assignment":
    st.text('Which assignment number would you like to review? (can be any existing assignment)')
    thisWeek()
    asst = int(st.number_input(''))
    for i in range(len(list(calendar.keys()))):
        if i == 2:
            st.text(f'{list(calendar.keys())[i]}: \t\t {calendar[list(calendar.keys())[i]][asst]}')
        else:  
            st.text(f'{list(calendar.keys())[i]}: \t {calendar[list(calendar.keys())[i]][asst]}')
  elif Action == "***SELECT ACTION***":
    st.text("Please select an action")

user = st.text_input('Username:','Zach')
year = st.selectbox('Year:',[2021,2022,2023])
semester = st.selectbox('Semester:',['Spring','Fall'])
filename = f'/{user}SchoolCalendar {semester} {year}.json'

dbx = initialize()
calendar = fromDBX(dbx,filename)

Action = st.selectbox("Select Action",["Assignments Due This Week", "Progress", "Adjust Assignment", "New Assignment", "Show Old Assignments", "Assignments Due This Month", "Show Assignments by Type", "Show Full Calendar","Review Single Assignment","Add Assignments from file","Assignments In Date Range"])
completeAction(Action)
