import dropbox, json, io
import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st

st.title("School Calendar")

def initialize():
  access = '8vYE9nXcBrIAAAAAAAAAASnG5cKRmMPdSMJiH-QximbXAXZR40C9EgmR1eZjYr9M'
  dbx = dropbox.Dropbox(access)
  dbx.users_get_current_account()
  return dbx

def toDBX(dbx, data,filename):
  with io.StringIO() as stream:
    json.dump(data, stream)
    stream.seek(0)
    dbx.files_upload(stream.read().encode(), filename, mode=dropbox.files.WriteMode.overwrite)

def fromDBX(dbx, filename):
  _, res = dbx.files_download(filename)
  with io.BytesIO(res.content) as stream:
    data = json.load(stream)
  return data 

class Huff():
    def encrypt(string):
        index = random.randint(0,1000)
        string = list(string)
        idx = pd.read_csv(f'https://raw.githubusercontent.com/Zachjaryw/Huffman/main/{index}.csv')
        left = idx['left'].values.tolist()
        right = idx['right'].values.tolist()
        stringList = []
        for position in string:
            for row in range(len(left)):
                if position in left[row]:
                    stringList.append('0')
                elif position in right[row]:
                    stringList.append('1')
        stringList.append(f':#{index}')
        return "".join(stringList)
            
    def decrypt(string):
        index = string[string.index(':')+2:]
        string = string[:string.index(':')]
        idx = pd.read_csv('https://raw.githubusercontent.com/Zachjaryw/Huffman/main/Huffman_Collected.csv')
        decrypt = [str(i)[:i.index(':')] for i in idx[str(index)].values.tolist()]
        values = [str(i) for i in idx['Find'].values.tolist()]
        stringList = []
        posIndex = 0
        while len(string) != 0:
            position = string[:posIndex+1]
            if position in decrypt:
                find = decrypt.index(string[:posIndex+1])
                stringList.append(values[find])
                string = string[posIndex+1:]
                posIndex = 0
            else:
                posIndex += 1
        return "".join(stringList)


    def encrypt_list(list_name):
      return [Huff.encrypt(str(item)) for item in list_name]

    def decrypt_list(list_name):
      return [Huff.decrypt(item) for item in list_name]

def setup_new_semester():
  global dbx
  global calendar
  global filename
  reset()
  toDBX(dbx, calendar, filename)

def save_cal():
  global calendar
  global data
  global dbx
  global user
  global filename
  global semester
  global year
  data[user][1][f'{semester} {year}'] = calendar
  toDBX(dbx, data, filename)

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
  df['Assignment Due Date'] = df['Assignment Due Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
  if df.empty == True:
    st.text(f'There are no assignments due until after {days_7}')
  else:
    st.text('Assignments:\n')
    st.dataframe(df[df['Assignment Type'] != 'Reading'])
    st.text('\nReadings:\n')
    st.dataframe(df[df['Assignment Type'] == 'Reading'])
  

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
    st.text('Assignments:\n')
    st.dataframe(df[df['Assignment Type'] != 'Reading'])
    st.text('\nReadings:\n')
    st.dataframe(df[df['Assignment Type'] == 'Reading'])

def adjust(entry_pos, column, input):
  global calendar
  calendar[column][entry_pos] = input
  st.text(f'Assignment position {entry_pos} adjusted')
  thisWeek()
  save_cal()

def classCode(class_code):
  global calendar
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
    thisWeek()
    st.text("Input Assignment position (or positions seperated by commas)")
    index = st.text_input("","",key = 0)
    if "," in index:
      positions = index.split(',')
      a = st.button("Submit",key = 17)
      if a == True:
        for pos in positions:
            progress(int(pos))
      else:
        pass
    else:
      st.text("Input new state or leave empty to mark complete")
      state = str(st.text_input("",key = 1))
      if state == "":
        if st.button("Submit",key = 18) == True:
            progress(index)
        else:
            pass
      else:
        if st.button("Submit", key = 19) == True:
            progress(index,state)
        else:
            pass
  elif Action == "Show Old Assignments":
    previousAst()
  elif Action == "Adjust Assignment":
    thisWeek()
    st.text("Input position of assignment to adjust")
    pos = int(st.text_input("",key = 2))
    st.text("Input the value for the column to adjust")
    for i in range(len(list(calendar.keys()))):
      st.text(f'{i}. {list(calendar.keys())[i]}')
    st.text('\n')
    col = int(st.text_input("",key = 3))
    while not(col >= 0 and col <= 5):
      st.text('Invalid input: please enter again')
      col = int(st.text_input("",key = 4))
    st.text("Input adjusted value")
    new = st.text_input("",key = 5)
    if st.button("Submit",key = 20) == True:
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
    else:
        pass
  elif Action == "Assignments Due This Week":
    thisWeek()
  elif Action == "Assignments Due This Month":
    thisMonth()
  elif Action == "New Assignment":
    st.text("New Assignment name")
    name = st.text_input("",key = 6)
    st.text("Class Code")
    code = st.text_input("",key = 7)
    st.text('Due Date')
    date = st.text_input("",key = 8)
    st.text('Notes (leave empty for default)')
    notes = str(st.text_input("",key = 9))
    st.text('Assignment Type (leave empty for default)')
    type_ = str(st.text_input("",key = 10))
    if st.button("Submit",key = 21) == True:
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
    else:
        pass
  elif Action == "Show Assignments by Type":
    st.text('Enter assignment type')
    type_ = st.text_input("",key = 11)
    if st.button("Submit",key = 22) == True:
        byType(type_)
    else:
        pass
  elif Action == "Add Assignments from file":
    st.text('Please enter the file path here:')
    st.text("The file must have correct column names: ['name','class_code','due_date','notes','status','ast_type']")
    filePath = st.text_input("",key = 12)
    if st.button("Submit",key = 23) == True:
        addAssignmentsFromFile(filePath)
    else:
        pass
  elif Action == "Assignments In Date Range":
    st.text('Enter the first (lower) date:')
    lowDate = st.text_input("",key = 13)
    st.text('Enter the second (higher) date:')
    highDate = st.text_input("",key = 14)
    if st.button("Submit",key = 24) == True:
        fromDateRange(lowDate,highDate)
    else:
        pass
  elif Action == "Review Single Assignment":
    st.text('Which assignment number would you like to review? (can be any existing assignment)')
    thisWeek()
    asst = int(st.text_input("",key = 15))
    for i in range(len(list(calendar.keys()))):
      if i == 2:
        st.text(f'{list(calendar.keys())[i]}: \t\t {calendar[list(calendar.keys())[i]][asst]}')
      else:  
        st.text(f'{list(calendar.keys())[i]}: \t {calendar[list(calendar.keys())[i]][asst]}')
  elif Action == "***SELECT ACTION***":
    st.text("Please select an action")


years = [2022,2023]
semesters = ['Spring','Fall']
filename = f'/SchoolCalendar.json'
user = st.text_input("Enter Username or type 'NEW' for a new user:")
dbx = initialize()
data = fromDBX(dbx,filename)
if user != 'NEW' and user in data.keys():
  acceptPassword = Huff.decrypt(data[user][0])
  password = st.text_input('Password:',"")
  if password == acceptPassword:
      year = st.selectbox('Year:',years)
      semester = st.selectbox('Semester:',semesters)
      calendar = data[user][1][f'{semester} {year}']
      Action = st.selectbox("Select Action",["Assignments Due This Week", "Progress", "Adjust Assignment", "New Assignment", "Show Old Assignments", "Assignments Due This Month", "Show Assignments by Type", "Show Full Calendar","Review Single Assignment","Add Assignments from file","Assignments In Date Range"])
      completeAction(Action)
elif user == "NEW":
  authorization = st.text_input('Enter developer authorization token to create new account:')
  if authorization == "activatenewaccount":
    newUsername = st.text_input('Enter your username here:')
    if newUsername in data.keys():
      st.text(f"Username, {newUsername}, is already taken. Please select a new username.")
    elif not(newUsername in data.keys()):
      password_1 = st.text_input('Enter your password here:')
      password_2 = st.text_input("Re-enter your password here:")
      if password_2 != "" and password_1 == password_2:
        newCal = {}
        for y in years:
          for sem in semesters:
            newCal[f'{sem} {y}'] = {
                                        'Assignment Name': [],
                                        'Assignment Due Date': [],
                                        'Class Code': [],
                                        'Assignment Notes': [],
                                        'Assignment Status': [],
                                        'Assignment Type': []
                                  }
        data[newUsername] = [password_1, newCal]
        toDBX(dbx, data, filename)
        st.text(f'New account for {newUsername} has been activated. \nChange username field at the top of the screen to begin.')
elif user not in data.keys():
  st.text("Enter Valid Username")



