#TO ADD- Have fetch tasks pass data into aggregate_task_data  



import dummy_data as gdd
import pandas as pd
import streamlit as st
import altair as alt   
import requests
import os
import json 
from datetime import datetime as dt, timedelta , timezone 

from dotenv import load_dotenv
load_dotenv()


def main():
    pass 
def fetching_tasks():
    click_up_api_key = os.getenv("cu_api_key")
    headers =   {"Authorization": click_up_api_key, 
                    "accept": "application/json",
                    "Content-Type": "application/json"}

    workspace_id = os.getenv("workspace_id")
    test_space_id = os.getenv("test_space")
    start_date = dt(2026, 4, 1, tzinfo=timezone.utc)
    end_date = dt(2026, 4, 21, tzinfo=timezone.utc)
    
    unix_converter = 1000


    # This line will get all of the tasks in your ws, I am just configuring with a test space get_tasks = requests.get(f"https://api.clickup.com/api/v2/team/{workspace_id}/task", headers=headers")
    get_tasks_request= requests.get(f'https://api.clickup.com/api/v2/team/{workspace_id}/task?space_ids[]={test_space_id}',headers=headers) 
    if get_tasks_request.status_code != 200:
        print(f"Task request API call failed. ERROR CODE: { get_tasks_request}")
    else:
        get_tasks_json = get_tasks_request.json().get("tasks")
    
    start_date_ms = int(start_date.timestamp() * unix_converter)
    end_date_ms = int(end_date.timestamp() * unix_converter)    
    get_entries_from_before_due_and_start_dates = requests.get(f'https://api.clickup.com/api/v2/team/{workspace_id}/time_entries?start_date={start_date_ms}&end_date={end_date_ms}', headers=headers)
    print(get_entries_from_before_due_and_start_dates.json().keys())
    if get_entries_from_before_due_and_start_dates.status_code != 200:
        print(f"Date filtered entries request API call failed, ERROR CODE: {get_entries_from_before_due_and_start_dates}")
    else:
        date_filtered_entries = get_entries_from_before_due_and_start_dates.json().get("data")
        if date_filtered_entries is None:
            print("No entries found")
        else:
            print(date_filtered_entries)
            
def aggregrate_task_data():
    pass
def display_views():
    def view_one():
        pass
    def view_two():
        pass
    def view_three():
        pass

fetching_tasks()