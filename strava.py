# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:30:47 2020

@author: dletran
"""
from pickle2 import save_object, load_object
import pandas as pd
import requests
import datetime
import os
from dotenv import load_dotenv

import matplotlib.pyplot as plt

#from selenium import webdriver
#from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC


class client:
    def __init__(self, auth_code=None):
        self.hd = None #headers
        self.bearer_token = None
        self.API_BASE = 'https://www.strava.com/api/v3/'
        self.__init_auth()
        self.__init_info()
        if auth_code is None: # if auth code passed to client, init bearer token
            print('Warning: no authorization code passed.')
            print("Initialize the client by passing the authorziation code.")
            self.__authorize()
        self.__init_bearer(auth_code)
        self.__get_token_scope()
        self.__store_headers()

        
    
    def __init_auth(self):
        load_dotenv('.env', override=True)
        self.auth = {'athlete_id' : 19925487, # Duke
                     'client_id' : os.environ.get('client_id'),
                     'client_secret' : os.environ.get('client_secret')} # 2021-02-13
        
        
    def __init_info(self):
        self.df_scopes = pd.Series({'read' : 'read public segments, public routes, public profile data, public posts, public events, club feeds, and leaderboards',
                                    'read_all': 'read private routes, private segments, and private events for the user',
                                    'profile:read_all' : 'read all profile information even if the user has set their profile visibility to Followers or Only You',
                                    'profile:write' : 'update the user\'s weight and Functional Threshold Power (FTP), and access to star or unstar segments on their behalf',
                                    'activity:read' : 'read the user\'s activity data for activities that are visible to Everyone and Followers, excluding privacy zone data',
                                    'activity:read_all' : 'the same access as activity:read, plus privacy zone data and access to read the user\'s activities with visibility set to Only You',
                                    'activity:write' : 'access to create manual activities and uploads, and access to edit any activities that are visible to the app, based on activity read access level'})
        self.df_scopes = self.df_scopes.reset_index()
        self.df_scopes.columns = ['scope', 'description']
    
    def __authorize(self):
        """ TO-DO: make this open via selenium to get the code"""
        print('https://www.strava.com/oauth/authorize?client_id=41942&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all')
        self.auth_code = input('Enter authorization code to continue >> ')
        
    def __init_bearer(self, auth_code):
        """
        STEP 2.
        You must get your authorization code first via browser. Reference README.
        This makes a request for your bearer_token information
        """
        if auth_code is None:
            auth_code = self.auth_code # provided by __authorize()
        pm = {'client_id' : self.auth['client_id'],
              'client_secret' : self.auth['client_secret'],
              'code' : auth_code,
              'grant_type' : 'authorization_code'}
        r = requests.post('https://www.strava.com/api/v3/oauth/token', params=pm)
        if r.ok:
            self.bearer_token = dict(r.json())
        
        return r
    
    def __store_headers(self):
        """prepares headers for api calls, pulled from bearer token"""
        token = pd.Series(self.bearer_token)
        auth_type = ' '.join(token[['token_type', 'access_token']])
        self.hd = {'authorization' : auth_type,
                   'accept' : 'application/json'} # store headers
        
    def __get_token_scope(self):
        """ gets token scope from user """
        print(self.df_scopes['scope'])
        while True:
            try:
                user_input = int(input('What is your token\'s scope? >> '))
            except ValueError:
                print('Please enter an int. Try again.')
                continue
            if user_input in self.df_scopes.index:
                break
        self.scope = self.df_scopes['scope'][user_input]
        


    # def check_token_exp(self):
    #     return True if self.s_token['expires_at'] < datetime.datetime.now() else False
    
    # def refresh_token(self):
    #     if self.check_token_exp:
    #         self._refresh_token()
    #     else:
    #         exp = self.token['expires_at']
    #         print(f'Token is not yet expired. Expiration at {exp}')
    
    # def _refresh_token(self):
    #     pm = {'client_id' : '41942',
    #           'client_secret' : 'd8a443fcdffe1fd7ab26b55edae19c96b35e7648',
    #           'refresh_token' : self.token['refresh_token'],
    #           'grant_type' : 'refresh_token'}
    #     r = requests.post('https://www.strava.com/api/v3/oauth/token', params=pm)
    #     r.ok
    #     if r.ok:
    #         s_token = pd.Series(r.json())
    #         s_token['expires_at'] = datetime.datetime.fromtimestamp(s_token['expires_at'])
    #         s_token['expires_in'] = datetime.timedelta(seconds=s_token['expires_in'])
    #         self.keychain.append(self.token) # save old token to keychain
    #         self.token = s_token
    #         self.init_bearer_token(s_token)
    #     else:
    #         print('Failed. Try again.')
    ##########################################################################
    ### API CALLS START HERE #################################################
    ##########################################################################
    def get_athlete(self):
        """gets info about athlete"""
        REQUEST_URL = self.API_BASE + 'athlete'
        r = requests.get(REQUEST_URL, 
                         headers=self.hd)
        return dict(r.json())
    
    def get_activities(self):
    # STEP 3: Test with activity
        pm =  {'per_page' : '100'}
        REQUEST_URL = self.API_BASE + 'athlete/activities'
        r = requests.get(REQUEST_URL,
                         params=pm,
                         headers=self.hd)
        return pd.DataFrame(data=r.json())
    

    def main():
        c = strava.client()
        c.get_athlete()
        df = c.get_activities()
        # convert to datetime
        for col in [x for x in df.columns if 'date' in x]:
            df[col] = pd.to_datetime(df[col])
            
        