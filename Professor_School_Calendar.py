import pandas as pd
import numpy as np
import dropbox, json, io
from Dropbox_Setup import *
from Huffman_Encryption import *
import streamlit as st
from Send_Message import *
import webbrowser

st.set_page_config(layout="wide")
st.title('Professor Assignment Calendar')

def add(course,name,date,notes,type_):
    current['Assignment Name'].append(name)
    current['Assignment Due Date'].append(str(date).replace('/','-'))
    current['Assignment Notes'].append(notes)
    current['Assignment Type'].append(type_)
    
def approveCourse(user):
    course = st.text_input('Please enter the course value in the correct format (ex: COMM330A-SPR22)',"",key = 2)
    approvedCourses = fromDBX(dbx,courseFilename)
    usernames = fromDBX(dbx,userFilename)
    if course in approvedCourses['Course'] and course != "":
        st.warning(f'Course {course} has already been approved for another professor. Please enter a new course')
    elif course != "" and not(course in usernames[user][1]):
        approvedCourses['Course'].append(course)
        approvedCourses['Professor'].append(user)
        usernames[user][1].append(course)
        toDBX(dbx,usernames,userFilename)
        st.text(f"{Huff.decrypt(user)}, you have now been approved as the professor for course {course}.")
        toDBX(dbx,approvedCourses,courseFilename)
        toDBX(dbx,
                {'Assignment Name': [],
                'Assignment Due Date': [],
                'Assignment Notes': [],
                'Assignment Type': []
                },f'{st.secrets.access.coursePath}{course}.json')
    else:
        st.warning('Please enter a couse value')

def completeAction(user,action):
    if action == 'Approve a New Course':
        approveCourse(acceptUser)
    elif action == 'Add Assignments':
        whichCourse = st.selectbox('Select a course:',['Select a Course']+fromDBX(dbx,userFilename)[user][1],key = 5)
        if whichCourse != 'Select a Course':
            with st.expander('From File (up to 100 assignments)'):
                if st.button('Dowload File'):
                    webbrowser.open_new_tab('https://github.com/Zachjaryw/School-Calendar/blob/main/Add_Assignments.xlsx?raw=true')
                file = st.file_uploader("Upload File Here",type = ['xlsx'])
                if file:
                    data = pd.read_excel(file,header = 2)
                    data.drop(0,inplace = True)
                    data.set_index(data.columns[0],inplace = True)
                    data.reset_index(inplace = True,drop = True)
                    data.drop(data.columns[4],axis = 1,inplace = True)
                    data['Assignment Due Date'] = [i[:10] for i in data['Assignment Due Date'].astype(str)]
                    counts = np.sum(list(data["Assignment Name"].value_counts(dropna = True)))
                    data = data[:counts]
                    current = fromDBX(dbx,f'{st.secrets.access.coursePath}{whichCourse}.json')
                    for row in range(data.shape[0]):
                        add(current,
                            data['Assignment Name'].iloc[row],
                            data['Assignment Due Date'].iloc[row],
                            data['Assignment Notes'].iloc[row],
                            data['Assignment Type'].iloc[row])
                    toDBX(dbx,current,f'{st.secrets.access.coursePath}{whichCourse}.json')
                    st.text(f'Assignments have been added to {whichCourse}')
                    st.experimental_rerun()
            with st.expander('Enter Assignment Here (up to 5 assignemnts)'):
                howManyAssignments = st.slider('How many assignments would you like to add?',1,5,key = 4)
                col0,col1,col2,col3,col4 = st.columns([1,4,2,4,2])
                col0.text('#')
                col1.text("Name")
                col2.text("Due Date")
                col3.text("Notes")
                col4.text("Type")
                for i in range(howManyAssignments):
                    col0,col1,col2,col3,col4 = st.columns([1,4,2,4,2])
                    col0.text(i)
                    exec(f'name{i} = col1.text_input("","",key = 100+i)')
                    exec(f'date{i} = col2.date_input("",key = 200+i)')
                    exec(f'notes{i} = col3.text_input("",key = 300+i)')
                    exec(f'type_{i} = col4.text_input("","Homework",key = 400+i)')
                if st.button('Submit',key = 3):
                    current = fromDBX(dbx,f'{st.secrets.access.coursePath}{whichCourse}.json')
                    for i in range(howManyAssignments):
                        exec(f"current['Assignment Name'].append(name{i})")
                        exec(f"current['Assignment Due Date'].append(str(date{i}).replace('/','-'))")
                        exec(f"current['Assignment Notes'].append(notes{i})")
                        exec(f"current['Assignment Type'].append(type_{i})")
                    toDBX(dbx,current,f'{st.secrets.access.coursePath}{whichCourse}.json')
                    st.text(f'Assignments have been added to {whichCourse}')
                    st.experimental_rerun()
    elif action == 'Review Assignments':
        whichCourse = st.selectbox('Select a course:',['Select a Course']+fromDBX(dbx,userFilename)[user][1],key = 1)
        if whichCourse != 'Select a Course':
            assignments = fromDBX(dbx,f'{st.secrets.access.coursePath}{whichCourse}.json')
            col0,col1,col2,col3,col4 = st.columns([1,4,2,4,2])
            col0.text('#')
            col1.text("Name")
            col2.text("Due Date")
            col3.text("Notes")
            col4.text("Type")
            for i in range(len(assignments['Assignment Name'])):
                col0,col1,col2,col3,col4 = st.columns([1,4,2,4,2])
                col0.text(i)
                col1.text(assignments['Assignment Name'][i])
                col2.text(assignments['Assignment Due Date'][i])
                col3.text(assignments['Assignment Notes'][i])
                col4.text(assignments['Assignment Type'][i])
    elif action == 'Adjust Assignments':
        st.warning('If your students have already added this assignment to their calendar, their assignment will not be updated')
        whichCourse = st.selectbox('Select a course:',['Select a Course']+fromDBX(dbx,userFilename)[user][1],key = 14)
        if whichCourse != 'Select a Course':
            assignments = fromDBX(dbx,f'{st.secrets.access.coursePath}{whichCourse}.json')
            col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,4,2,1])
            col0.text('#')
            col1.text("Name")
            col2.text("Due Date")
            col3.text("Notes")
            col4.text("Type")
            col5.text('Remove')
            removeButtons = []
            for i in range(len(assignments['Assignment Name'])):
                col0,col1,col2,col3,col4,col5 = st.columns([1,4,2,4,2,1])
                col0.text(i)
                col1.text(assignments['Assignment Name'][i])
                col2.text(assignments['Assignment Due Date'][i])
                col3.text(assignments['Assignment Notes'][i])
                col4.text(assignments['Assignment Type'][i])
                exec(f"button{i} = col5.button('Remove',key = 400+{i})")
                exec(f"removeButtons.append(button{i})")
            if True in removeButtons:
                index = removeButtons.index(True)
                for key in assignments.keys():
                    assignments[key].remove(assignments[key][index])
                toDBX(dbx,assignments,f'{st.secrets.access.coursePath}{whichCourse}.json')
                st.text('Assignment has been removed')
                st.experimental_rerun()
            adjustPosition = st.selectbox('Which value would you like to adjust?',['Assignment Name','Assignment Due Date','Assignment Notes','Assignment Type'],key = 20)
            assignmentNumber = st.text_input('Which assignment would you like to adjust?',"0",key = 21)
            if adjustPosition == "Assignment Due Date":
                newValue = st.date_input("Please enter new value",key = 22)
            else:
                newValue = st.text_input("Please enter new value",key = 23)
            if st.button("Submit",key = 24):
                if adjustPosition == "Assignment Due Date":
                    assignments[adjustPosition][int(assignmentNumber)] = str(newValue).replace('/','-')
                else:
                    assignments[adjustPosition][int(assignmentNumber)] = newValue
                toDBX(dbx,assignments,f'{st.secrets.access.coursePath}{whichCourse}.json')
                st.text("Value has been changed")
                st.experimental_rerun()
    elif action == 'Remove Course':
        whichCourse = st.selectbox('Select a course:',['Select a Course']+fromDBX(dbx,userFilename)[user][1],key = 18)
        if whichCourse != 'Select a Course':
            if st.text_input(f'Please type "delete course {whichCourse}" to remove the course') == f"delete course {whichCourse}" and st.button('Remove Course'):
                deleteFile(dbx,f'{st.secrets.access.coursePath}{whichCourse}.json')
                usernames = fromDBX(dbx,userFilename)
                usernames[user][1].remove(whichCourse)
                toDBX(dbx,usernames,userFilename)
                c = fromDBX(dbx,courseFilename)
                index = c['Course'].index(whichCourse)
                c['Course'].remove(whichCourse)
                c['Professor'].remove(c['Professor'][index])
                toDBX(dbx,c,courseFilename)
                st.text(f'Course {whichCourse} has been deleted')
                st.experimental_rerun()
            

userFilename = st.secrets.files.userFilename
courseFilename = st.secrets.files.courseFilename
findCourse = st.secrets.access.coursePath
dbx = initializeToken(st.secrets.access.access)
usernames = fromDBX(dbx,userFilename)
user = st.text_input("Enter Username or type 'NEW' for a new user:",key = 6)
decrypted = Huff.decryptList(list(usernames.keys()))
if user != 'NEW' and user in decrypted:
  acceptUser = list(usernames.keys())[decrypted.index(user)]
  acceptPassword = Huff.decrypt(usernames[acceptUser][0])
  with st.expander('Password',expanded = True):
    password = st.text_input("",key = 7)
  if password == acceptPassword:
      selectAction = st.selectbox('Select an Action',['Review Assignments','Adjust Assignments','Add Assignments','Approve a New Course',"Remove Course"],key = 8)
      completeAction(acceptUser,selectAction)
elif user == "NEW":
  authorization = st.text_input('Please type the authorization code here:',"access-",key = 9)
  accessToken = fromDBX(dbx,'/AccessToken.json')
  if st.button('Press to generate access code',key = 10):
      accessToken = randomMessage()
      toDBX(dbx, accessToken,'/AccessToken.json')
      st.text(f'An access token has been sent to the developer. Message {st.secrets.phoneNumbers.to} for access.')
  if authorization == st.secrets.access.accessToken or authorization == f'access-{accessToken}':
    newUsername = st.text_input('Enter your username here:',key = 11)
    if newUsername == '':
      st.text('Please enter a valid username.')
    elif newUsername in decrypted:
      st.text(f"Username, {newUsername}, is already taken. Please select a new username.")
    elif not(newUsername in decrypted):
      password_1 = st.text_input('Enter your password here:',key = 12)
      password_2 = st.text_input("Re-enter your password here:",key = 13)
      if password_2 != "" and password_1 == password_2:
        usernames[Huff.encrypt(newUsername)] = [Huff.encrypt(password_1),[]]
        toDBX(dbx, usernames, userFilename)
        st.text(f'New account for {newUsername} has been activated. \nChange username field at the top of the screen to begin.')
  else:
    st.text('Please Enter Auth Key from Developer')
elif user not in decrypted:
  st.warning("Enter Valid Username")
