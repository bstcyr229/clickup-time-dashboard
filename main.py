
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt   
import requests
import os
import json 
import holidays 

from datetime import datetime as dt, timedelta , timezone 

from dotenv import load_dotenv
load_dotenv()



def user_input():
        start_date = st.datetime_input(label="Please enter start date", format="YYYY/MM/DD", value=dt(2026, 4, 1, tzinfo=timezone.utc))
        end_date =  st.datetime_input(label="Please enter end date", format="YYYY/MM/DD", value=dt(2026, 5, 1, tzinfo=timezone.utc) )
        dates_tuple = start_date, end_date
        return dates_tuple
def fetching_tasks(dates_tuple):
        start_date = dates_tuple[0]
        end_date = dates_tuple[1]
        
        
        click_up_api_key = os.getenv("cu_api_key")
        headers =   {"Authorization": click_up_api_key, 
                        "accept": "application/json",
                        "Content-Type": "application/json"}

        workspace_id = os.getenv("workspace_id") #This will cause the API to only pull from one workspace
        
        if workspace_id is None:
            return ("No workspace ID")
        test_space_id = os.getenv("test_space")
        
        get_tasks_json = []
        date_filtered_entries = []
        user_teams_json = []
        tasks_and_entries_tuple = ()


        us_holidays = holidays.US()


        date_differences = end_date - start_date
        total_work_days = date_differences.days
        
        
        date_differences_delta = range(total_work_days)
        
        for day in date_differences_delta:
            if (start_date + timedelta(days=day)).date().weekday() >= 5 or (start_date + timedelta(days=day)).date() in us_holidays:
                total_work_days -= 1

        
        unix_converter = 1000
        mileseconds_converter = 3600000

        get_user_teams_request = requests.get(f"https://api.clickup.com/api/v2/group?team_id={workspace_id }", headers=headers)
        if get_user_teams_request.status_code != 200:
            return (f"User group request API call failed. ERROR CODE: {get_user_teams_request}")    
        else:
            user_teams_json = get_user_teams_request.json().get("groups")
            
        if user_teams_json == []:
            st.text("No user groups found")
            return ("No user groups found")
        # This endpoint will get all of the tasks in your ws, I am just configuring with a test space get_tasks = requests.get(f"https://api.clickup.com/api/v2/team/{workspace_id}/task", headers=headers")
        get_tasks_request= requests.get(f'https://api.clickup.com/api/v2/team/{workspace_id}/task?space_ids[]={test_space_id}',headers=headers) 
        
        if get_tasks_request.status_code != 200:
            return (f"Task request API call failed. ERROR CODE: { get_tasks_request}")
        else:
            get_tasks_json = get_tasks_request.json().get("tasks")
            
            if get_tasks_json == []:
                st.text("No tasks found")
                return("No tasks found")
            
        
        start_date_ms = int(start_date.timestamp() * unix_converter)
        end_date_ms = int(end_date.timestamp() * unix_converter)
        
        get_entries_from_before_due_and_start_dates = requests.get(f'https://api.clickup.com/api/v2/team/{workspace_id}/time_entries?start_date={start_date_ms}&end_date={end_date_ms}', headers=headers)
            

        date_filtered_entries_json = get_entries_from_before_due_and_start_dates.json().get("data")    

        if get_entries_from_before_due_and_start_dates.status_code != 200:
            return st.text(f"Date filtered entries request API call failed, ERROR CODE: {get_entries_from_before_due_and_start_dates}")
        else:
            date_filtered_entries_json = get_entries_from_before_due_and_start_dates.json().get("data")
            
            if date_filtered_entries_json == []:
                st.text("No entries found for that date range, please re-enter a new date")
                return "No entries found for that date range, please re-enter a new date"
            else:
                tasks_and_entries_tuple = (date_filtered_entries_json , get_tasks_json, user_teams_json, total_work_days)
                return tasks_and_entries_tuple
                
def aggregrate_task_data(tasks_and_entries_tuple):
        unix_converter = 1000
        mileseconds_converter = 3600000
        
        entries_json = tasks_and_entries_tuple [0]
        tasks_json = tasks_and_entries_tuple[1]
        user_groups_json = tasks_and_entries_tuple[2]
        total_work_days = tasks_and_entries_tuple[3]
        
        user_groups_df = pd.json_normalize(user_groups_json) 
        user_groups_df = user_groups_df.explode('members')
        user_groups_df["team_name"] = user_groups_df['name']
        user_groups_df["team_member"] = user_groups_df['members'].apply(lambda x: x.get("username") if isinstance(x,dict) and len(x) > 0 else None)
        user_groups_df["team_member_id"] = user_groups_df['members'].apply(lambda x: x.get("id") if isinstance(x,dict) and len(x) > 0 else None)
        user_groups_df["team_member_id"] = user_groups_df['team_member_id'].astype('Int64')
        user_groups_df_filtered = user_groups_df[[
            'team_name',
            'team_member',
            'team_member_id',
        ]].copy 
        
        tasks_df = pd.json_normalize(tasks_json)
        tasks_df['time_estimate'] = tasks_df['time_estimate'].astype("Int64") / mileseconds_converter
        tasks_df['time_spent'] = tasks_df['time_spent'].astype("Int64") / mileseconds_converter
        tasks_df['task_start_date'] = tasks_df['start_date'].apply( lambda x: dt.fromtimestamp(int(x) / unix_converter).date().isoformat() if x is not None and pd.notna(x) else "No date found")
        tasks_df['task_due_date'] = tasks_df['due_date'].apply( lambda x: dt.fromtimestamp(int(x) / unix_converter).date().isoformat() if x is not None and pd.notna(x) else "No date found")
        tasks_df["user_id"] = tasks_df['assignees'].apply(lambda x: x[0].get("id") if isinstance(x,list) and len(x) > 0 else None )
        tasks_df['team_member'] = tasks_df['assignees'].apply(lambda x: x.get('username') if isinstance(x,dict) else None)
        tasks_df['team_member_id'] = tasks_df['assignees'].apply(lambda x: x.get('id') if isinstance(x,dict) else None)
        tasks_df['task_id'] = tasks_df['id']
        tasks_df['task_name'] = tasks_df['name']
        
        task_df_filtered = tasks_df[[
            'task_id',
            'task_name', 
            'team_member',
            'team_member_id',
            'time_estimate',
            'time_spent',
            'task_start_date', 
            'task_due_date'
        ]].copy()


        entries_df = pd.json_normalize(entries_json)
        entries_df['duration'] = entries_df['duration'].astype('Int64') / mileseconds_converter 
        entries_df['entry_date'] = entries_df['start'].apply( lambda x: dt.fromtimestamp(int(x) / unix_converter).date().isoformat() if x is not None else "No date found") # Getting the date for each entry
        entries_df['non_billable'] = np.where(entries_df['billable'] != True, entries_df['duration'],0)
        entries_df['billable_hours'] = np.where(entries_df['billable'] == True, entries_df['duration'], 0 )
        entries_df['actual_hours'] = entries_df[['non_billable', 'billable_hours']].sum(axis=1)
        entries_df['task_name'] = entries_df['task.name']
        entries_df['task_id'] = entries_df['task.id']
        entries_df['team_member'] = entries_df['user.username']
        entries_df['team_member_id'] = entries_df['user.id'].astype("Int64")
        

        final_df = entries_df[[
            'team_member',
            'team_member_id',
            'task_name',
            'task_id',
            'entry_date',
            'billable_hours',
            'non_billable',
            'actual_hours'
        ]].copy()
        
        
        final_df = final_df.merge(user_groups_df[["team_name", "team_member_id"]] , on="team_member_id")
        final_df = final_df.merge(tasks_df[["time_estimate", "task_id"]], on="task_id")
        final_df = final_df.merge(tasks_df[["task_start_date", "task_id"]], on="task_id")
        final_df = final_df.merge(tasks_df[["task_due_date", "task_id"]], on="task_id")
        dates_and_final_df = (final_df , total_work_days)
        return dates_and_final_df 

def display_views(dates_and_final_df):
        final_df = dates_and_final_df[0]
        total_work_days = dates_and_final_df[1]
        final_df = final_df.sort_values(by='entry_date')

        


        def view_one():
            #Team View 
            work_day_duration = 8
            rounder = 100 
            team_members =  final_df.groupby("team_name")["team_member"].unique()
            team_estimated_hours_worked =  final_df.groupby("team_name")["time_estimate"].sum()
            team_actual_hours_worked = final_df.groupby("team_name")["actual_hours"].sum()
            team_billable_hours = final_df.groupby("team_name")["billable_hours"].sum()
            
            total_hours = team_members.apply(len) * (total_work_days * work_day_duration) 
            over_capacity = total_hours < team_actual_hours_worked
            over_capacity_percentage = round(((team_actual_hours_worked / total_hours ) * rounder) - rounder)
            team_register_hours = final_df.groupby("team_name")["actual_hours"].sum()
            
            
            teams = final_df["team_name"].unique()
            cols = st.columns(len(teams))

            for i, team in enumerate(teams):
                with cols[i]:
                    st.metric(label=f"{team} Capacity", value=total_hours[team])
            for i, team in enumerate(teams):
                with cols[i]:
                    st.metric(label=f"{team} Actual Hours Worked", value=team_actual_hours_worked[team], delta=f"{over_capacity_percentage[team]:+.2f}%")
            for i, team in enumerate(teams):
                with cols[i]:
                    st.metric(label=f"{team} Billable to Actual", value=f"{(team_actual_hours_worked[team] / team_billable_hours[team] ):.2f}")    
        
            hours_worked_by_team_and_day = pd.DataFrame({"Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable Hours Worked": team_billable_hours, "Overcapacity":over_capacity})
            st.title("Team View")
            st.dataframe(data= hours_worked_by_team_and_day)
            
            hours_worked_by_team_and_day = pd.DataFrame({ "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable Hours Worked": team_billable_hours, "Overcapacity":over_capacity})
        
            days_seperated_for_graph = final_df.groupby(["team_name", "entry_date"])["actual_hours"].sum().unstack().transpose().reset_index()
            st.write("Days to Hours Worked by Team")
            st.area_chart(data=days_seperated_for_graph, x='entry_date', y=[team], width='stretch') 

        def view_two():
            #Staff member drill down 
            team_member_estimated_hours_worked = final_df.groupby("team_member")["time_estimate"].sum()
            team_member_actual_hours_worked = final_df.groupby("team_member")["actual_hours"].sum()
            team_member_total_hours_worked = final_df.groupby("team_member")["actual_hours"].sum()
            capacity_check = team_member_total_hours_worked > (total_work_days * 8)
            team_member_tasks_worked = final_df.groupby("team_member")["task_name"].agg(list)
            data_by_team_member = pd.DataFrame({"Tasks": team_member_tasks_worked, "Estimated Hours": team_member_estimated_hours_worked, "Actual Hours Worked": team_member_actual_hours_worked, "Billable Hours Worked":final_df.groupby("team_member")['billable_hours'].sum(), "Overcapacity": capacity_check})
            st.title("View by Employee")
            st.title("Team Member Metrics at a Glance")
            
            team_members = final_df["team_member"].unique()
            cols = st.columns(len(team_members))


            for i, team_member in enumerate(team_members):
                with cols[i]:
                    st.metric(label="Team Member Average Estimated Hours Worked", value=f"{team_member_estimated_hours_worked.mean():.2f}")
            for i, team_member in enumerate(team_members):
                with cols[i]:
                    st.metric(label="Team Member Average Actual Hours Worked", value=f"{team_member_actual_hours_worked.mean():.2f}")
            for i, team_member in enumerate(team_members):
                with cols[i]:
                    st.metric(label="Team Member Average Billable Hours Worked", value=f"{(final_df.groupby('team_member')['billable_hours'].sum()).mean():.2f}")   
            
            st.dataframe(data_by_team_member , width='stretch')
            
            
            chart_data = pd.DataFrame({"Assignee": final_df.groupby("team_member").first().index, "Estimated": team_member_estimated_hours_worked, "Actual": team_member_actual_hours_worked, "Billable": final_df.groupby("team_member")['billable_hours'].sum()}).reset_index()
            st.title("Team Memebers: Estimated, Actual and Billable Hours")
            color_scale = alt.Scale(domain=["Estimated", "Actual", "Billable"], range=["#1f77b4", "#ff7f0e", "#2ca02c"])

            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X("Assignee:N"),
                y=alt.Y("value:Q"),
                color=alt.Color("variable:N", scale=color_scale),
                xOffset="variable:N"
            ).transform_fold(["Estimated", "Actual", "Billable"], as_=["variable", "value"])
            st.altair_chart(chart, width='stretch')
        def view_three():
            tasks_for_view_three = final_df["task_name"]
            task_ids_for_view_three = final_df["task_id"]
            task_estimated_hours = final_df["time_estimate"]
            task_actual_hours = final_df["actual_hours"]
            task_assignee = final_df["team_member"]
            task_to_billable = final_df["billable_hours"]
            table_for_view_three = pd.DataFrame({"Tasks": tasks_for_view_three, "Task Id": task_ids_for_view_three, "Assignee":task_assignee, "Estimated Hours": task_estimated_hours, "Actual Hours":task_actual_hours,"Billable":task_to_billable, }).set_index("Tasks")
            table_for_chart_three = pd.DataFrame({"Tasks": tasks_for_view_three, "Task Id": task_ids_for_view_three, "Assignee":task_assignee, "Estimated Hours": task_estimated_hours, "Actual Hours":task_actual_hours,"Billable":task_to_billable, })
            st.title("View by Tasks")
        
            st.title("Task Metrics at a Glance")
            col1, col2, col3 = st.columns(3)
            with col1:
                    st.metric(label="Average Estimated Hours per Task", value=f"{task_estimated_hours.mean():.2f}")
            with col2:
                    st.metric(label="Average Actual Hours per Task", value=f"{task_actual_hours.mean():.2f}")
            with col3:
                    st.metric(label="Average Billable Hours per Task", value=f"{task_to_billable.mean():.2f}")
            chart = alt.Chart(table_for_chart_three).mark_bar().encode( 
                    x=alt.X("Tasks:N"),
                    y=alt.Y("value:Q"),
                    color=alt.Color("variable:N", scale=alt.Scale(domain=["Estimated Hours", "Actual Hours", "Billable"] , range=["#1f77b4", "#ff7f0e", "#2ca02c"])),
                    xOffset="variable:N").transform_fold(["Estimated Hours", "Actual Hours","Billable"], as_=["variable", "value"])
            st.dataframe(table_for_view_three)
            st.title("Tasks: Estimated, Actual and Billable Hours")
            st.altair_chart(chart, use_container_width=True)
        
        # user_input = ""
        # user_input = st.text_input(label="Please input date: Year, Month, Day")


        genre = st.radio(
        "Which view would you like to see",
        ["View One: Team View", "View Two: View by Assignee", "View Three: Project/Task View"],
        index=None,
    )


        if genre == None:
            st.write("Please select a view")


        elif genre == "View One: Team View":
            view_one() 

        elif genre == "View Two: View by Assignee":
            view_two() 

        elif genre == "View Three: Project/Task View":
            view_three()
        else: 
            st.write("You selected:", genre)
        
#aggregrate_task_data(fetching_tasks(user_input()))
display_views(aggregrate_task_data(fetching_tasks(user_input())))