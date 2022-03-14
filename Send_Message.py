from twilio.rest import Client
import streamlit as st

'''
sendMessage method is used to text a desired message to the authorized phone number
@param message:str. any string that will be sent to the authorized number
@return message. the message is returned back.
'''
def sendMessage(message:str):
    client = Client(st.secrets.twilio.accountSID,st.secrets.twilio.authToken)
    client.messages.create(to= st.secrets.phoneNumbers.to,
                           from_ = st.secrets.phoneNumbers.from_,
                           body = message)
    return message

'''
sendMessage method is used to text a randomized message to the authorized phone number
@return message. the message is returned back.
'''
def randomMessage():
    message = []
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    for i in range(6):
      message.append(possible[np.random.randint(0,len(possible))])
    message = "".join(message)
    client = Client(st.secrets.twilio.accountSID,st.secrets.twilio.authToken)
    client.messages.create(to= st.secrets.phoneNumbers.to,
                           from_ = st.secrets.phoneNumbers.from_,
                           body = f"A new user would like to setup an account. Access token: {message}")
    return message
