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
    print(user_groups_df["members"].head())
    user_groups_df["team name"] = user_groups_df['name']
    user_groups_df["team member"] = user_groups_df['members'].apply(lambda x: x.get("username") if isinstance(x,dict) and len(x) > 0 else None)
    user_groups_df["team member id"] = user_groups_df['members'].apply(lambda x: x.get("id") if isinstance(x,dict) and len(x) > 0 else None)
    user_groups_df["team member id"] = user_groups_df['team member id'].astype('Int64')
    user_groups_df_filtered = user_groups_df[[
        'team name',
        'team member',
        'team member id',
    ]].copy 
    
    tasks_df = pd.json_normalize(tasks_json)
    tasks_df['time estimate'] = tasks_df['time_estimate'].astype("Int64") / mileseconds_converter
    tasks_df['time_spent'] = tasks_df['time_spent'].astype("Int64") / mileseconds_converter
    tasks_df['task start date'] = tasks_df['start_date'].astype("Int64") /mileseconds_converter  
    tasks_df['task due date'] = tasks_df['due_date'].astype('Int64') / mileseconds_converter
    tasks_df["user id"] = tasks_df['assignees'].apply(lambda x: x[0].get("id") if isinstance(x,list) and len(x) > 0 else None)
    tasks_df['team member'] = tasks_df['assignees'].apply(lambda x: x.get('username') if isinstance(x,dict) else None)
    tasks_df['team member id'] = tasks_df['assignees'].apply(lambda x: x.get('id') if isinstance(x,dict) else None)
    tasks_df['task id'] = tasks_df['id']
    tasks_df['task name'] = tasks_df['name']
    
    task_df_filtered = tasks_df[[
        'task id',
        'task name', 
        'team member',
        'team member id',
        'time estimate',
        'time_spent',
        'task start date', 
        'task due date'
    ]].copy()

    entries_df = pd.json_normalize(entries_json)
    entries_df['duration'] = entries_df['duration'].astype('Int64') / mileseconds_converter   
    entries_df['entry date'] = entries_df['at'].apply( lambda x: dt.fromtimestamp(int(x) / unix_converter).date().isoformat()) # Getting the date for each entry
    entries_df['non-billable'] = np.where(entries_df['billable'] != True, entries_df['duration'],0)
    entries_df['billable_hours'] = np.where(entries_df['billable'] == True, entries_df['duration'], 0 )
    entries_df['task name'] = entries_df['task.name']
    entries_df['task id'] = entries_df['task.id']
    entries_df['team member'] = entries_df['user.username']
    entries_df['team member id'] = entries_df['user.id'].astype("Int64")
    

    final_df = entries_df[[
        'team member',
        'team member id',
        'task name',
        'task id',
        'entry date',
        'billable_hours',
        'non-billable'
    ]].copy()
    
    
    final_df = final_df.merge(user_groups_df[["team name", "team member id"]] , on="team member id")
    final_df = final_df.merge(tasks_df[["time estimate", "task id"]], on="task id")
    # final_df = final_df.merge(tasks_df[["task start date", "task id"]], on="task id")
    # final_df = final_df.merge(tasks_df[["task due date", "task id"]], on="task id")


    print(final_df)
    return final_df
def display_views(final_df):
    pass 
    def view_one():
        pass
        # team_members =  user_groups_filtered.groupby("Team")["team member"].unique()
        # team_estimated_hours_worked =  task_df.groupby("Team")["estimated_hours"].sum()
        # team_actual_hours_worked = entries_df.groupby("Team")["actual_hours"].sum()
        # team_billable_hours = entries_df.groupby("Team")["billable_hours"].sum()
        
        # total_hours = team_members.apply(len) * 40
        # over_capacity = total_hours < team_actual_hours_worked
        # over_capacity_percentage = round(((team_actual_hours_worked / total_hours ) * 100) - 100 )
        # team_register_hours = dummy_data_keys.groupby("Team")["actual_hours"].sum()
        
        # days = dummy_data_keys.groupby("Team")["day"].agg(list)
        

    
#     col1, col2, col3 = st.columns(3)
#     col4, col5, col6 = st.columns(3)
#     col7, col8, col9 = st.columns(3)
    
#     with col1:
#         st.metric(label="Team 1 Total Capacity", value=f"{total_hours['Team One']}")
#     with col2:
#         st.metric(label="Team 2 Total Capacity", value=f"{total_hours['Team Two']}")
#     with col3:
#         st.metric(label="Team 3 Total Capacity", value=f"{total_hours['Team Three']}")
#     with col4:
#         st.metric(label="Team 1 Actual Hours Worked", value=f"{team_actual_hours_worked['Team One']}", delta=f"{over_capacity_percentage['Team One']:+.2f}%")
#     with col5:
#         st.metric(label="Team 2 Actual Hours Worked", value=f"{team_actual_hours_worked['Team Two']}", delta=f"{over_capacity_percentage['Team Two']:+.2f}%")
#     with col6:
#         st.metric(label="Team 3 Actual Hours Worked", value=f"{team_actual_hours_worked['Team Three']}", delta=f"{over_capacity_percentage['Team Three']:+.2f}%")
#     with col7:
#         st.metric(label="Team 1 Billable to Actual", value=f"{(team_billable_hours['Team One'] / team_actual_hours_worked['Team One']):.2f}")
#     with col8:
#         st.metric(label="Team 2 Billable to Actual", value=f"{(team_billable_hours['Team Two'] / team_actual_hours_worked['Team Two']):.2f}")
#     with col9:
#         st.metric(label="Team 3 Billable to Actual", value=f"{team_billable_hours['Team Three']/ team_actual_hours_worked['Team Three']:.2f}")
    
    
    
#     hours_worked_by_team_and_day = pd.DataFrame({"Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable Hours Worked": team_billable_hours, "Overcapacity":over_capacity})
#     st.title("Team View")
#     st.dataframe(data= hours_worked_by_team_and_day)
    
#     hours_worked_by_team_and_day = pd.DataFrame({ "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable Hours Worked": team_billable_hours, "Overcapacity":over_capacity})
    
#     days_seperated_for_graph = dummy_data_keys.groupby(["Team", "day"])["actual_hours"].sum().unstack().transpose().reset_index()
#     st.write("Days to Hours Worked by Team")
#     st.area_chart(data=days_seperated_for_graph, x="day", y=["Team One", "Team Two", "Team Three"], use_container_width=True) 

    def view_two():
        pass
    def view_three():
        pass

display_views(aggregrate_task_data(fetching_tasks()))