import dropbox, json, io
import streamlit as st

'''
method initialize sets up access to a dropbox
@return dbx. an open access token to the desired dropbox
'''
def initialize():
  access = st.secrets.access.access
  dbx = dropbox.Dropbox(access)
  dbx.users_get_current_account()
  return dbx

'''
method initializeToken sets up access to a dropbox from new access token
@param token. dropbox app access token
@return dbx. an open access token to the desired dropbox
'''
def initializeToken(token):
  access = token
  dbx = dropbox.Dropbox(access)
  dbx.users_get_current_account()
  return dbx

'''
method toDBX allows for files to be written and rewritten to dropbox
@param dbx. initialization variable
@param data. what information you would like to put in the desired file.
    this is converted to a json format so must be a json, dict, or string/int
@param filename. the path within dropbox that you would like to insert the data
'''
def toDBX(dbx, data,filename):
  with io.StringIO() as stream:
    json.dump(data, stream)
    stream.seek(0)
    dbx.files_upload(stream.read().encode(), filename, mode=dropbox.files.WriteMode.overwrite)

'''
method fromDBX allows for files to be accessed from dropbox
@param dbx. initialization variable
@param filename. the parth within dropbox that you would like to access
@return data. the data in a json format that is associated with the selected filename
'''
def fromDBX(dbx, filename):
  _, res = dbx.files_download(filename)
  with io.BytesIO(res.content) as stream:
    data = json.load(stream)
  return data

def deleteFile(dbx,filename):
  dbx.files_delete(filename)
