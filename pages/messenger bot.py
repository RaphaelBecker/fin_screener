import streamlit as st
from PIL import Image
# from https://www.geeksforgeeks.org/send-message-to-telegram-user-using-python/
# importing all required libraries
#import telebot
#from telethon.sync import TelegramClient
#from telethon.tl.types import InputPeerUser, InputPeerChannel
#from telethon import TelegramClient, sync, events

st.write("# Here you can set up your Alerts")

# Set up sections of web page
header = st.container()
set_up = st.container()
running_bots = st.container()

with header:
    with st.expander('How to set up alerts?'):
        st.markdown(
        '''
        1. Open the telegram app and search for @BotFather.
        2. Click on the start button or send “/start”.
        3. Then send “/newbot” message to set up a name and a username.
        4. After setting name and username BotFather will give you an API token which is your bot token. 
        '''
        )
        image = Image.open('mocks/telegram_bot.png')
        st.image(image, caption='How to')

with set_up:
    with st.expander('Set up a new instance'):
        api_id = st.text_input('api_id')
        st.write('The api_id is', api_id)

        api_hash = st.text_input('api_hash')
        st.write('The api_hash is', api_hash)

        token = st.text_input('token')
        st.write('The token is', token)

        phone = st.text_input('phone number')
        st.write('The phone is', phone)

        st.button('Create instance')

with running_bots:
    with st.expander('Manage your running instances'):
        for i in range(0,2,1):
            form = st.form(key=f"Instance {i}")
            form.text('XYZ Stategy to my oncle')
            col1, col2, col3 = st.columns((1, 1, 1))
            with col1:
                start_button = form.form_submit_button(label='start')
            with col2:
                stop_button = form.form_submit_button(label='stop')
            with col3:
                delete_button = form.form_submit_button(label='delete')





# get your api_id, api_hash, token
# from telegram as described above
# api_id = 'API_id'
# api_hash = 'API_hash'
# token = 'bot token'
message = "Working..."

# your phone number
phone = 'YOUR_PHONE_NUMBER_WTH_COUNTRY_CODE'

# creating a telegram session and assigning
# it to a variable client
#client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
#client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
#if not client.is_user_authorized():
#    client.send_code_request(phone)

    # signing in the client
#    client.sign_in(phone, input('Enter the code: '))

#try:
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
#    receiver = InputPeerUser('user_id', 'user_hash')

    # sending message using telegram client
#    client.send_message(receiver, message, parse_mode='html')
#except Exception as e:

    # there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
#    print(e);

# disconnecting the telegram session
#client.disconnect()
