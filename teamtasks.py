
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
def fetching_tasks():
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
workspace_id = os.getenv("workspace_id")
test_space = os.getenv("test_space")
headers = {"Authorization": click_up_api_key}

get_tasks = requests.get(f"https://api.clickup.com/api/v2/team/{workspace_id}/task", headers=headers, params={"team_ids[]": [test_space]})
get_tasks_json = get_tasks.json().get("tasks")
print(get_tasks_json)

list_of_user_groups = []