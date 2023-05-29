import requests, random, csv, os, re, time
from datetime import datetime
import difflib
import os.path
from post_photo_scr import *
from parsing_google_sheets import *
from config import *

# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
# credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#
# SAMPLE_SPREADSHEET_ID = table_id
##
# SAMPLE_RANGE_NAME = list
#
# service = build('sheets', 'v4', credentials=credentials)
v = 5.131