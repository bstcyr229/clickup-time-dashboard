#NEXT- Construct view one based on entries and user groups (teams in ClickUp UI)
#Evening session 4/22/26
    # type cast my task_df columns to int so the milisecond converter will work 



import dummy_data as gdd
import numpy as np
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
    
    if workspace_id is None:
        print("No workspace ID")
    test_space_id = os.getenv("test_space")
    
    get_tasks_json = []
    date_filtered_entries = []
    user_teams_json = []
    tasks_and_entries_tuple = ()
    
    start_date = dt(2026, 4, 1, tzinfo=timezone.utc)
    end_date = dt(2026, 4, 21, tzinfo=timezone.utc)
    unix_converter = 1000
    mileseconds_converter = 3600000

    get_user_teams_request = requests.get(f"https://api.clickup.com/api/v2/group?team_id={workspace_id }", headers=headers)
    if get_user_teams_request.status_code != 200:
        print(f"User group request API call failed. ERROR CODE: {get_user_teams_request}")    
    else:
        user_teams_json = get_user_teams_request.json().get("groups")
    if user_teams_json is None:
        print("No user groups found")
    # This line will get all of the tasks in your ws, I am just configuring with a test space get_tasks = requests.get(f"https://api.clickup.com/api/v2/team/{workspace_id}/task", headers=headers")
    get_tasks_request= requests.get(f'https://api.clickup.com/api/v2/team/{workspace_id}/task?space_ids[]={test_space_id}',headers=headers) 
    
    if get_tasks_request.status_code != 200:
        print(f"Task request API call failed. ERROR CODE: { get_tasks_request}")
    else:
        get_tasks_json = get_tasks_request.json().get("tasks")
    
    start_date_ms = int(start_date.timestamp() * unix_converter)
    end_date_ms = int(end_date.timestamp() * unix_converter)    
    get_entries_from_before_due_and_start_dates = requests.get(f'https://api.clickup.com/api/v2/team/{workspace_id}/time_entries?start_date={start_date_ms}&end_date={end_date_ms}', headers=headers)
    
    if get_entries_from_before_due_and_start_dates.status_code != 200:
        print(f"Date filtered entries request API call failed, ERROR CODE: {get_entries_from_before_due_and_start_dates}")
    else:
        date_filtered_entries_json = get_entries_from_before_due_and_start_dates.json().get("data")
        if date_filtered_entries is None:
            print("No entries found")
        else:
            tasks_and_entries_tuple = (date_filtered_entries_json , get_tasks_json, user_teams_json)
            return tasks_and_entries_tuple
            
def aggregrate_task_data(tasks_and_entries_tuple):
    unix_converter = 1000
    mileseconds_converter = 3600000
    
    entries_json = tasks_and_entries_tuple [0]
    tasks_json = tasks_and_entries_tuple[1]
    user_groups_json = tasks_and_entries_tuple[2]

    user_groups_df = pd.json_normalize(user_groups_json) 
    user_groups_df = user_groups_df.explode('members')
    # user_groups_df["username"] = user_groups_df['members'].apply(lambda x: x["username"]) 
    user_groups_df["team name"] = user_groups_df['name']
    user_groups_df["username"] = user_groups_df['members'].apply(lambda x: x.get("username") if isinstance(x,dict) else None)

    user_groups_df_filtered = user_groups_df[[
        'team name',
        'username'
    ]].copy 
    print(user_groups_df_filtered)
    
    tasks_df = pd.json_normalize(tasks_json)
    tasks_df['time_estimate'] = tasks_df['time_estimate'].astype("Int64") / mileseconds_converter
    tasks_df['time_spent'] = tasks_df['time_spent'].astype("Int64") / mileseconds_converter
    tasks_df['start_date'] = tasks_df['start_date'].astype("Int64") /mileseconds_converter  
    tasks_df['due_date'] = tasks_df['due_date'].astype('Int64') / mileseconds_converter

    
    task_df_filtered = tasks_df[[
        'id', #task id
        'name', # task name
        'time_estimate',
        'time_spent',
        'start_date', 
        'due_date'
    ]].copy()
    
    entries_df = pd.json_normalize(entries_json)
    entries_df['duration'].astype('Int64')    
    
    entries_df['non-billable'] = np.where(entries_df['billable'] != True, entries_df['duration'],0).astype(int) / mileseconds_converter
    entries_df['billable_hours'] = np.where(entries_df['billable'] == True, entries_df['duration'], 0 ).astype(int) / mileseconds_converter
    
    entries_df_filtered_for_billable = entries_df[[
        'user.username',
        'user.id',
        'task.name',
        'at',
        'billable_hours',
        'non-billable'




    ]].copy()
    
def display_views():
    def view_one():
        pass
    def view_two():
        pass
    def view_three():
        pass

aggregrate_task_data(fetching_tasks())