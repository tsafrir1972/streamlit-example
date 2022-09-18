from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import random
import base64
import re
from email.message import EmailMessage
import ssl
import smtplib

import requests
import os
import json
import pymongo




class TravelOptions:

    def __init__(self):

        self.get_user_input()

    def get_user_input(self):
        global selected_city
        global selected_flight_budget
        global selected_hotel_budget
        global selected_restorants_budget
        global user_email
        #global df_list_airports
        #global df_airports
        #global app_flights
        global our_email
        ############################### city choose ################################

        def get_base64(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()

        def set_background(png_file):
            bin_str = get_base64(png_file)
            page_bg_img = '''
                    <style>
                    .stApp {
                    background-image: url("data:image/png;base64,%s");
                    background-size: cover;
                    }
                    </style>
                    ''' % bin_str
            st.markdown(page_bg_img, unsafe_allow_html=True)

        set_background(r"my_trip.png")

        st.title("Travel Planning Application")
        # gc = geonamescache.GeonamesCache()
        # cities = gc.get_cities()

        selected_city = st.selectbox(
            'Enter Your Travel City : ',
            ('New York','San Francisco','Honolulu', 'Bankok', 'Barcelona', 'Dubai', 'Paris', 'london', 'Tel Aviv'))

        ############################### flight budget choose ########################

        global selected_flight_budget

        selected_flight_budget = st.selectbox(
            'Enter Your Flight Budget : ',
            ('500', '1000', '1500'))

        ########################### Hotel Budget Choose ######################################
        global selected_hotel_budget

        selected_hotel_budget = st.selectbox(
            'Enter Your Hotel Budget : ',
            ('50', '100', '150'))
        ########################### Restorants Budget Choose ######################################
        global selected_restorants_budget

        selected_restorants_budget = st.selectbox(
            'Enter Your Restorant Budget : ',
            ('50', '100', '150'))
        ########################### Enter Email ######################################
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        check_email = 'N'
        keys = random.sample(range(1000, 9999), 1)

        def check(email):

            if (re.fullmatch(regex, email)):

                check_email = 'Y'


            else:

                check_email = 'N'

            return check_email

        form = st.form(key='my_form')
        user_email = form.text_input(label='Enter Your Email', key=1)
        submit_button = form.form_submit_button(label='Submit')


        # user_email = st.text_input('Please Enter Your Email :')
        for i in keys:
            if submit_button:
                # print(check(user_email))

                if check(user_email) == 'N':
                    st.write('The email is invalid please type again and press submit')
                    None
                else:
                    self.Process_User_Input()
                    self.send_to_user_email(user_email)
                    break
                    
    def Process_User_Input(self):

        with st.spinner('Your Vacation Is On Its Way,Please Wait...'):
            
            uri = "mongodb://192.168.248.244:27017"       
            myclient = pymongo.MongoClient(uri)
            mydb = myclient["travel_app"]
            mycol = mydb["Flights"]
            
            
            
            
            
            #app_flights = Flights().find_flight(selected_city)
            #app_hotels = Hotels().find_hotels(selected_city)
            #app_restorants = Restorants().find_restorants(selected_city)
            time.sleep(5)
        st.success('Done! Please Check Your Email For Your Vacation Recommendations for ' +  selected_city + '(Your Flights Are Listed Below) ')
        st.balloons()

    def send_to_user_email(self, user_email):

            email_sender = 'travel.app.flyer@gmail.com'
            email_password = 'efotfjtutkrsxzby'
            email_receiver = user_email

            subject = 'Check out your travel recommendations for ' + selected_city
            #flights_list = ' '.join(map(str,df_list_airports))
            body = "Test"
            #body = "Your Recommended Flights - " + flights_list + "\n" + "Your Recommended Hotels  - " + flights_list + "\n" + "Your Recommended Restorants - " + flights_list
            #body = "Your Recommended Travel Information Are - \n\n\n" + "\n\n FLIGHTS \n\n " + df_airports_string + "\n\n HOTELS \n\n " + df_hotels_string + "\n\n RESTORANTS \n\n " + df_restorants_string
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

        #print('Application process finished !')            

if __name__ == '__main__':

    TravelOptions()
