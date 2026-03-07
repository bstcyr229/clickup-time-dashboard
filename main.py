#Which of your teams is over or under capacity right now
#A deep dive on each of the members of your team, who is under capacity and who isn't
#An analysis of individual tasks, time spent vs time estimated 
#ClickUp API documentation link https://developer.clickup.com/reference/gettimeentrieswithinadaterange

import dummy_data as gdd
import pandas as pd
import streamlit as st
import altair as alt   
import requests
import os 


from dummy_data import generate_dummy_data

dummy_data_keys = gdd.generate_dummy_data()



def view_one():
    team_members = dummy_data_keys.groupby("Team")["assignee"].unique()
    team_members_number = team_members.apply(len)
    team_estimated_hours_worked = dummy_data_keys.groupby("Team")["estimated_hours"].sum()
    team_actual_hours_worked = dummy_data_keys.groupby("Team")["actual_hours"].sum()
    team_billable_hours = dummy_data_keys.groupby("Team")["billable_hours"].sum()
    total_hours = team_members_number * 40
    over_capacity = total_hours < team_actual_hours_worked
    over_capacity_percentage = round(((team_actual_hours_worked / total_hours ) * 100) - 100 )
    team_register_hours = dummy_data_keys.groupby("Team")["actual_hours"].sum()
    
    days = dummy_data_keys.groupby("Team")["day"].agg(list)
    

    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    
    with col1:
        st.metric(label="Team 1 Total Capacity", value=f"{total_hours['Team One']}")
    with col2:
        st.metric(label="Team 2 Total Capacity", value=f"{total_hours['Team Two']}")
    with col3:
        st.metric(label="Team 3 Total Capacity", value=f"{total_hours['Team Three']}")
    with col4:
        st.metric(label="Team 1 Actual Hours Worked", value=f"{team_actual_hours_worked['Team One']}", delta=f"{over_capacity_percentage['Team One']:+.2f}%")
    with col5:
        st.metric(label="Team 2 Actual Hours Worked", value=f"{team_actual_hours_worked['Team Two']}", delta=f"{over_capacity_percentage['Team Two']:+.2f}%")
    with col6:
        st.metric(label="Team 3 Actual Hours Worked", value=f"{team_actual_hours_worked['Team Three']}", delta=f"{over_capacity_percentage['Team Three']:+.2f}%")
    with col7:
        st.metric(label="Team 1 Billable to Actual", value=f"{(team_billable_hours['Team One'] / team_actual_hours_worked['Team One']):.2f}")
    with col8:
        st.metric(label="Team 2 Billable to Actual", value=f"{(team_billable_hours['Team Two'] / team_actual_hours_worked['Team Two']):.2f}")
    with col9:
        st.metric(label="Team 3 Billable to Actual", value=f"{team_billable_hours['Team Three']/ team_actual_hours_worked['Team Three']:.2f}")
    
    
    
    hours_worked_by_team_and_day = pd.DataFrame({"Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable Hours Worked": team_billable_hours, "Overcapacity":over_capacity})
    st.title("Team View")
    st.dataframe(data= hours_worked_by_team_and_day)
    
    hours_worked_by_team_and_day = pd.DataFrame({ "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable Hours Worked": team_billable_hours, "Overcapacity":over_capacity})
    
    days_seperated_for_graph = dummy_data_keys.groupby(["Team", "day"])["actual_hours"].sum().unstack().transpose().reset_index()
    st.write("Days to Hours Worked by Team")
    st.area_chart(data=days_seperated_for_graph, x="day", y=["Team One", "Team Two", "Team Three"], use_container_width=True) 

def view_two():
    assignee_estimated_hours_worked = dummy_data_keys.groupby("assignee")["estimated_hours"].sum()
    assignee_actual_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    assignee_total_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    capacity_check = assignee_total_hours_worked > 40
    assignee_tasks_worked = dummy_data_keys.groupby("assignee")["task"].agg(list)
    data_by_assignee = pd.DataFrame({"Tasks": assignee_tasks_worked, "Estimated Hours": assignee_estimated_hours_worked, "Actual Hours Worked": assignee_actual_hours_worked, "Billable Hours Worked":dummy_data_keys.groupby("assignee")['billable_hours'].sum(), "Overcapacity": capacity_check})
    st.title("View by Employee")
    st.title("Assignee Metrics at a Glance")
    col1, col2, col3 = st.columns(3)
    #col4, col5, col6 = st.columns(3)
    
    with col1:
        st.metric(label="Assignee Average Estimated Hours Worked", value=f"{assignee_estimated_hours_worked.mean():.2f}")
    with col2:
        st.metric(label="Assignee Average Actual Hours Worked", value=f"{assignee_actual_hours_worked.mean():.2f}")
    with col3:
        st.metric(label="Assignee Average Billable Hours Worked", value=f"{(dummy_data_keys.groupby('assignee')['billable_hours'].sum()).mean():.2f}")   
    
    st.dataframe(data_by_assignee)
    
    
    chart_data = pd.DataFrame({"Assignee": dummy_data_keys.groupby("assignee").first().index, "Estimated": assignee_estimated_hours_worked, "Actual": assignee_actual_hours_worked, "Billable": dummy_data_keys.groupby("assignee")['billable_hours'].sum()}).reset_index()
    st.title("Assignees: Estimated, Actual and Billable Hours")
    color_scale = alt.Scale(domain=["Estimated", "Actual", "Billable"], range=["#1f77b4", "#ff7f0e", "#2ca02c"])

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("Assignee:N"),
        y=alt.Y("value:Q"),
        color=alt.Color("variable:N", scale=color_scale),
        xOffset="variable:N"
    ).transform_fold(["Estimated", "Actual", "Billable"], as_=["variable", "value"])
    st.altair_chart(chart, use_container_width=True)

def view_three():
    
    tasks_for_view_three = dummy_data_keys["task"]
    task_ids_for_view_three = dummy_data_keys["task_id"]
    task_estimated_hours = dummy_data_keys["estimated_hours"]
    task_actual_hours = dummy_data_keys["actual_hours"]
    task_assignee = dummy_data_keys["assignee"]
    task_to_billable = dummy_data_keys["billable_hours"]
    task_cost = task_actual_hours * dummy_data_keys["hourly_rate"]
    table_for_view_three = pd.DataFrame({"Tasks": tasks_for_view_three, "Task Id": task_ids_for_view_three, "Assignee":task_assignee, "Estimated Hours": task_estimated_hours, "Actual Hours":task_actual_hours,"Billable":task_to_billable, "Cost":task_cost  }).set_index("Tasks")
    table_for_chart_three = pd.DataFrame({"Tasks": tasks_for_view_three, "Task Id": task_ids_for_view_three, "Assignee":task_assignee, "Estimated Hours": task_estimated_hours, "Actual Hours":task_actual_hours,"Billable":task_to_billable, "Cost":task_cost  })
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
        xOffset="variable:N"

    ).transform_fold(["Estimated Hours", "Actual Hours","Billable"], as_=["variable", "value"])
    st.dataframe(table_for_view_three)
    st.title("Tasks: Estimated, Actual and Billable Hours")
    st.altair_chart(chart, use_container_width=True)

st.title("ClickUp Time Tracker Dashboard")

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

