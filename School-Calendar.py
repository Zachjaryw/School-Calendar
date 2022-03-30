import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st
from Huffman_Encryption import * #access encryption software
from Dropbox_Setup import * #access dropbox
from Send_Message import * #access message sending

st.set_page_config(layout="wide")
st.title("School Calendar")

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
  global acceptUser
  global filename
  global semester
  global year
  data[acceptUser][1][f'{semester} {year}'] = calendar
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

def thisWeekPositions():
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  days_7 = str(dt.date.today() + dt.timedelta(weeks = 1))
  df = df[df['Assignment Due Date'] <= days_7]
  df = df[df['Assignment Status'] != 'Complete']
  df['Assignment Due Date'] = df['Assignment Due Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
  return df.index.values.tolist()

def fromDateRangePositions(lowDate, highDate):
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  df = df[df['Assignment Due Date'] >= lowDate][df['Assignment Due Date'] <= highDate]
  df['Assignment Due Date'] = df['Assignment Due Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
  return df.index.values.tolist()

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

def thisMonthPositions():
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  month_1 = str(dt.date.today() + dt.timedelta(month = 1))
  df = df[df['Assignment Due Date'] <= month_1]
  df = df[df['Assignment Status'] != 'Complete']
  df['Assignment Due Date'] = df['Assignment Due Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
  return df.index.values.tolist()

def adjust(entry_pos, column, input):
  global calendar
  calendar[column][entry_pos] = input
  st.text(f'Assignment position {entry_pos} adjusted')
  save_cal()
  
def previousAstPositions():
  global calendar
  df = pd.DataFrame(calendar)
  df['Assignment Due Date'] = pd.to_datetime(df['Assignment Due Date'])
  df.sort_values('Assignment Due Date',inplace = True)
  df = df[df['Assignment Status'] == 'Complete']
  df['Assignment Due Date'] = df['Assignment Due Date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d'))
  return df.index.values.tolist()

def progress(index_pos, stage = 'Complete'):
  global calendar
  calendar['Assignment Status'][int(index_pos)] = str(stage)
  st.text(f"Assignment {str(calendar['Assignment Name'][int(index_pos)])} is now marked as {stage}")
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
  if Action == "Show Old Assignments":
    setupPreviousAssignments()
  elif Action == "Adjust Assignment":
    setupCompleteAssignments()
    st.text("Input position of assignment to adjust")
    pos = st.text_input('Assignment Position',"0",key = 2)
    pos = int(pos)
    col = st.selectbox("Select Which Column:",['Assignment Name','Assignment Due Date','Class Code','Assignment Notes','Assignment Status','Assignment Type'])
    new = st.text_input("Input adjusted value",key = 5)
    if st.button("Submit",key = 20) == True:
        if col == 'Assignment Name':
          adjust(pos,'Assignment Name',new)
        elif col == 'Assignment Due Date':
          adjust(pos,'Assignment Due Date',new)
        elif col == 'Class Code':
          adjust(pos,'Class Code',new)
        elif col == 'Assignment Notes':
          adjust(pos,'Assignment Notes',new)
        elif col == 'Assignment Status':
          adjust(pos,'Assignment Status',new)
        elif col == 'Assignment Type':
          adjust(pos,'Assignment Type',new)
    else:
        pass
  elif Action == "Assignments Due This Week":
    setupCompleteAssignments()
  elif Action == "Assignments Due This Month":
    setupCompleteAssignmentsMonth()
  elif Action == "New Assignment":
    name = st.text_input("New Assignment name","",key = 6)
    code = st.text_input("Class Code","",key = 7)
    date = st.text_input('Due Date',"",key = 8)
    notes = str(st.text_input('Notes (leave empty for default)',"",key = 9))
    type_ = str(st.text_input('Assignment Type (leave empty for default)',"",key = 10))
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
  elif Action == "Assignments In Date Range":
    st.text('Enter the first (lower) date:')
    lowDate = st.text_input("",key = 13)
    st.text('Enter the second (higher) date:')
    highDate = st.text_input("",key = 14)
    if st.button("Submit",key = 24) == True:
        setupDateRangeAssignments(lowDate,highDate)
    else:
        pass
  elif Action == "Course Assignmenets":
      whichCourse = st.selectbox('Select a course:',['Select a Course']+data[acceptUser][2][f'{semester} {year}'],key=27)
      if whichCourse != 'Select a Course':
          assignments = fromDBX(dbxProf,f'{st.secrets.access.coursePath}{whichCourse}.json')
          col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,4,2,2])
          col0.text('#')
          col1.text("Name")
          col2.text("Due Date")
          col3.text("Notes")
          col4.text("Type")
          col5.text("Add to Calendar")
          addButtons = []
          for i in range(len(assignments['Assignment Name'])):
              col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,4,2,2)
              col0.text(i)
              col1.text(assignments['Assignment Name'][i])
              col2.text(assignments['Assignment Due Date'][i])
              col3.text(assignments['Assignment Notes'][i])
              col4.text(assignments['Assignment Type'][i])
              exec(f'addButton{i} = col5.button("Add",key = 25000+{i})')
              exec(f'addButtons.append(addButton{i})')
          if True in addButtons:
              index = addButtons.index(True)
              add(assignments['Assignment Name'][index],
                  whichCourse,
                  assignments['Assignment Due Date'][index],
                  assignments['Assignment Notes'][index],
                  'Incomplete',
                  assignments['Assignment Type'][index])
  elif Action == "My Courses":
      courses = fromDBX(dbxProf,st.secrets.file.courseFilename)
      cos = []
      for i in range(len(data[acceptUser][2][f'{semester} {year}'])):
        col1,col2,col3 = st.columns([4,4,2])
        col1.text(courses['Course'][index])
        col2.text(Huff.decrypt(courses['Professor'][index]))
        exec(f'but_{i} = col3.button("Unenroll",key = 30000+{i})')
        exec(f'cos.append(but_{i})')
        if True in cos:
          unenrolled = courses['Course'][cos.index(True)]
          st.text(f'You are now unenrolled in {unenrolled}')
          data[acceptUser][2][f'{semester} {year}'].remove(unenrolled)
          save_cal()
          st.experimental_rerun()
      course = st.text_input('Enter the code for the course you would like to join:',"",key = 26)
      if course in data[acceptUser][2][f'{semester} {year}']:
          st.text('You are already enrolled in this course')
      elif course in courses['Course']:
          st.text(f'You are now enrolled in {course}')
          idx = courses['Course'].index(course)
          courses['Students'][idx].append(acceptUser)
          toDBX(dbxProf,courses,st.secrets.file.courseFilename)
          data[acceptUser][2][f'{semester} {year}'].append(course)
          save_cal()
      else:
          st.warning('This course does not exist: Please consult your professor')
  elif Action == "***SELECT ACTION***":
    st.text("Please select an action")

class assignment:
    def __init__(self,position:int):
        global calendar
        self.position = position
        self.name = calendar['Assignment Name'][position]
        self.due = calendar['Assignment Due Date'][position]
        self.code = calendar['Class Code'][position]
        self.note = calendar['Assignment Notes'][position]
        self.status = calendar['Assignment Status'][position]
        self.type_ = calendar['Assignment Type'][position]

    def completeAssignment(self):
        global calendar
        progress(self.position)
        st.text(f'{self.position} marked complete')

    def incompleteAssignment(self):
        global calendar
        progress(self.position,"Incomplete")
        st.text(f'{self.position} marked Incomplete')        
        
    def adjustAssignment(self,column,newValue):
        adjust(self.position,column,newValue)
        st.text(f'Value {self.position} in {column} adjusted.')
        st.experimental_rerun()
        
    def printValues(self):
        st.text(f'Item Position:          {self.position}')
        st.text(f'Name:                   {self.name}')
        st.text(f'Due Date:               {self.due}')
        st.text(f'Class Code:             {self.code}')
        st.text(f'Notes:                  {self.note}')
        st.text(f'Status:                 {self.status}')
        st.text(f'Type:                   {self.type_}')
        

def setupCompleteAssignments():
  col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
  col0.text("#")
  col1.text("Name")
  col2.text("Due Date")
  col3.text("Class Code")
  col4.text("Complete")
  col5.text("Assignment Details")
  completeButtons = []
  fullButtons = []
  for item in thisWeekPositions():
      exec(f'a{item} = assignment(item)')
      with st.container():
          col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
          exec(f'col0.text(a{item}.position)')
          exec(f'col1.text(a{item}.name)')
          exec(f'col2.text(a{item}.due)')
          exec(f'col3.text(a{item}.code)')
          exec(f"completeButton{item} = col4.button('Complete',key = {10000+item})")
          exec(f"completeButtons.append(completeButton{item})")
          exec(f"fullButton{item} = col5.button('Full Assignment',key = {item+20000})")
          exec(f"fullButtons.append(fullButton{item})")
  if True in completeButtons:
    exec(f'a{thisWeekPositions()[completeButtons.index(True)]}.completeAssignment()')
    st.experimental_rerun()
  elif True in fullButtons:
    exec(f'a{thisWeekPositions()[fullButtons.index(True)]}.printValues()')

def setupCompleteAssignmentsMonth():
  col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
  col0.text("#")
  col1.text("Name")
  col2.text("Due Date")
  col3.text("Class Code")
  col4.text("Complete")
  col5.text("Assignment Details")
  completeButtons = []
  fullButtons = []
  for item in thismonthPositions():
      exec(f'a{item} = assignment(item)')
      with st.container():
          col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
          exec(f'col0.text(a{item}.position)')
          exec(f'col1.text(a{item}.name)')
          exec(f'col2.text(a{item}.due)')
          exec(f'col3.text(a{item}.code)')
          exec(f"completeButton{item} = col4.button('Complete',key = {10000+item})")
          exec(f"completeButtons.append(completeButton{item})")
          exec(f"fullButton{item} = col5.button('Full Assignment',key = {item+20000})")
          exec(f"fullButtons.append(fullButton{item})")
  if True in completeButtons:
    exec(f'a{thismonthPositions()[completeButtons.index(True)]}.completeAssignment()')
    st.experimental_rerun()
  elif True in fullButtons:
    exec(f'a{thismonthPositions()[fullButtons.index(True)]}.printValues()')

def setupPreviousAssignments():
  col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
  col0.text("#")
  col1.text("Name")
  col2.text("Due Date")
  col3.text("Class Code")
  col4.text("Incomplete")
  col5.text("Assignment Details")
  completeButtons = []
  fullButtons = []
  for item in previousAstPositions():
      exec(f'a{item} = assignment(item)')
      with st.container():
          col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
          exec(f'col0.text(a{item}.position)')
          exec(f'col1.text(a{item}.name)')
          exec(f'col2.text(a{item}.due)')
          exec(f'col3.text(a{item}.code)')
          exec(f"completeButton{item} = col4.button('Incomplete',key = {10000+item})")
          exec(f"completeButtons.append(completeButton{item})")
          exec(f"fullButton{item} = col5.button('Full Assignment',key = {item+20000})")
          exec(f"fullButtons.append(fullButton{item})")
  if True in completeButtons:
    exec(f'a{previousAstPositions()[completeButtons.index(True)]}.incompleteAssignment()')
    st.experimental_rerun()
  elif True in fullButtons:
    exec(f'a{previousAstPositions()[fullButtons.index(True)]}.printValues()')

def setupDateRangeAssignments(lowDate,highDate):
  col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
  col0.text("#")
  col1.text("Name")
  col2.text("Due Date")
  col3.text("Class Code")
  col4.text("Complete")
  col5.text("Assignment Details")
  completeButtons = []
  fullButtons = []
  for item in fromDateRangePositions(lowDate, highDate):
      exec(f'a{item} = assignment(item)')
      with st.container():
          col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,1.5,2,2])
          exec(f'col0.text(a{item}.position)')
          exec(f'col1.text(a{item}.name)')
          exec(f'col2.text(a{item}.due)')
          exec(f'col3.text(a{item}.code)')
          exec(f"completeButton{item} = col4.button('Complete',key = {10000+item})")
          exec(f"completeButtons.append(completeButton{item})")
          exec(f"fullButton{item} = col5.button('Full Assignment',key = {item+20000})")
          exec(f"fullButtons.append(fullButton{item})")
  if True in completeButtons:
    exec(f'a{fromDateRangePositions(lowDate, highDate)[completeButtons.index(True)]}.completeAssignment()')
    st.experimental_rerun()
  elif True in fullButtons:
    exec(f'a{fromDateRangePositions(lowDate, highDate)[fullButtons.index(True)]}.printValues()')


years = [2022,2023]
semesters = ['Spring','Fall']
filename = st.secrets.file.filename
user = st.text_input("Enter Username or type 'NEW' for a new user:")
dbx = initialize()
dbxProf = initializeToken(st.secrets.access.accessProfessor)
data = fromDBX(dbx,filename)
decrypted = Huff.decryptList(list(data.keys()))
if user != 'NEW' and user in decrypted:
  acceptUser = list(data.keys())[decrypted.index(user)]
  acceptPassword = Huff.decrypt(data[acceptUser][0])
  with st.expander('Password',expanded = True):
    password = st.text_input("")
  if password == acceptPassword:
      with st.expander("Year and Semester Selection"):
        year = st.selectbox('Year:',years)
        semester = st.selectbox('Semester:',semesters)
      calendar = data[acceptUser][1][f'{semester} {year}']
      Action = st.selectbox("Select Action",["Assignments Due This Week", "New Assignment", "Adjust Assignment", "Show Old Assignments","Assignments In Date Range","Course Assignmenets","My Courses"])     #["Assignments Due This Week", "Progress", "Adjust Assignment", "New Assignment", "Show Old Assignments", "Assignments Due This Month", "Show Assignments by Type", "Show Full Calendar","Review Single Assignment","Add Assignments from file","Assignments In Date Range"])
      completeAction(Action)
elif user == "NEW":
  authorization = st.text_input('Please type the authorization code here:',"access-")
  if st.button('Press to generate access code'):
      accessToken = randomMessage()
      toDBX(dbx, accessToken,'/AccessToken.json')
      st.text(f'An access token has been sent to the developer. Message {st.secrets.phoneNumbers.to} for access.')
  if authorization == st.secrets.access.accessToken or authorization == ('access-' + str(fromDBX(dbx,'/AccessToken.json'))):
    newUsername = st.text_input('Enter your username here:')
    if newUsername == '':
      st.text('Please enter a valid username.')
    elif newUsername in decrypted:
      st.text(f"Username, {newUsername}, is already taken. Please select a new username.")
    elif not(newUsername in decrypted):
      password_1 = st.text_input('Enter your password here:')
      password_2 = st.text_input("Re-enter your password here:")
      if password_2 != "" and password_1 == password_2:
        newCal = {}
        enrollment = {}
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
            enrollment[f'{sem} {y}'] = []
        data[Huff.encrypt(newUsername)] = [Huff.encrypt(password_1), newCal,enrollment]
        toDBX(dbx, data, filename)
        st.text(f'New account for {newUsername} has been activated. \nChange username field at the top of the screen to begin.')
  else:
    st.text('Please Enter Auth Key from Developer')
elif user not in decrypted:
  st.text("Enter Valid Username")
