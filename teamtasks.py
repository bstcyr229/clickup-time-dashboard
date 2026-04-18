
import dummy_data as gdd
import pandas as pd
import streamlit as st
import altair as alt   
import requests
import os
import json 
from datetime import datetime as dt 
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()


def main():
    pass 
def fetching_workspace_id():
    pass
def fetching_teams_and_tasks():
    pass
def aggregrate_task_data():
    pass
def display_views():
    def view_one():
        pass
    def view_two():
        pass
    def view_three():
        pass

click_up_api_key = os.getenv("cu_api_key")
headers = {"Authorization": click_up_api_key}

get_workspace_id= requests.get("https://api.clickup.com/api/v2/team", headers=headers)
print(f" the type of get_workspace_id is {type(get_workspace_id)}")
workspace_data = get_workspace_id.json().get("teams")
print(workspace_data)

list_of_user_groups = []

for team in workspace_data:
    team_id = team["id"]
    group_request =  requests.get("https://api.clickup.com/api/v2/group",headers=headers, params = {"team_id":team_id})
    json_of_groups = group_request.json().get("groups")
    
    for team_id in json_of_groups:
        list_of_user_groups.append(json_of_groups[1]["team_id"])


        for team_id in  list_of_user_groups:
            task_request= requests.get(f"https://api.clickup.com/api/v2/team/{team_id}/task", headers=headers)
            tasks_json = task_request.json().get("tasks")
