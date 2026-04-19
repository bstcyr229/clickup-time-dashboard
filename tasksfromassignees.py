
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
headers = {"Authorization": click_up_api_key}

workspace_id = os.getenv("workspace_id")
test_space_id = os.getenv("test_space")


milisecond_converter = 3600000
unix_converter = 1000


# This line will get all of the tasks in your ws, I am just configuring with a test space get_tasks = requests.get(f"https://api.clickup.com/api/v2/team/{workspace_id}/task", headers=headers")
get_tasks= requests.get(f'https://api.clickup.com/api/v2/team/{workspace_id}/task?space_ids[]={test_space_id}',headers=headers) 
get_tasks_json = get_tasks.json().get("tasks")

# get_entries = requests.get(f"")
