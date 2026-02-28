#Which of your teams is over or under capacity right now
#A deep dive on each of the members of your team, who is under capacity and who isn't
#An analysis of individual tasks, time spent vs time estimated 
#ClickUp API link https://developer.clickup.com/reference/gettimeentrieswithinadaterange

import dummy_data as gdd
import pandas as pd
import streamlit as st


from dummy_data import generate_dummy_data

dummy_data_keys = gdd.generate_dummy_data()
team_register_two = dummy_data_keys.groupby("Team")["assignee"].unique()


def view_one():
    team_members = dummy_data_keys.groupby("Team")["assignee"].unique()
    team_members_number = team_members.apply(len)
    team_estimated_hours_worked = dummy_data_keys.groupby("Team")["estimated_hours"].sum()
    team_actual_hours_worked = dummy_data_keys.groupby("Team")["actual_hours"].sum()
    difference_in_hours = team_actual_hours_worked - team_estimated_hours_worked
    total_hours = team_members_number * 40
    over_capacity = total_hours < team_actual_hours_worked
    over_capacity_percentage = round(((team_actual_hours_worked / total_hours ) * 100) - 100 )
    team_register_hours = dummy_data_keys.groupby("Team")["actual_hours"].sum()
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    with col1:
        st.metric(label="Team One Total Hours", value=f"{total_hours['Team One']}")
    with col2:
        st.metric(label="Team Two Total Hours", value=f"{total_hours['Team Two']}")
    with col3:
        st.metric(label="Team Three Total Hours", value=f"{total_hours['Team Three']}")
    with col4:
        st.metric(label="Team One Actual Hours Worked", value=f"{team_actual_hours_worked['Team One']}", delta=f"{over_capacity_percentage['Team One']}%")
    with col5:
        st.metric(label="Team Two Actual Hours Worked", value=f"{team_actual_hours_worked['Team Two']}", delta=f"{over_capacity_percentage['Team Two']}%")
    with col6:
        st.metric(label="Team Three Actual Hours Worked", value=f"{team_actual_hours_worked['Team Three']}", delta=f"{over_capacity_percentage['Team Three']}%")
    hours_by_team = pd.DataFrame({"Team Members":team_register_hours, "Team Capacity": total_hours , "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Difference": difference_in_hours, "Overcapacity":over_capacity, "Over Capacity Percentage" : over_capacity_percentage})
    st.title("Team View")
    st.dataframe(data=hours_by_team)
    st.area_chart(data=hours_by_team,x="Team Members", y=["Estimated Hours Worked", "Actual Hours Worked"])
    #Add in graphs to show the overcapacity percentage for each team, and the difference in hours between estimated and actual hours worked.
    
def view_two():
    assignee_estimated_hours_worked = dummy_data_keys.groupby("assignee")["estimated_hours"].sum()
    assignee_actual_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    assginee_total_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    capacity_check = assginee_total_hours_worked > 40
    assignee_tasks_worked = dummy_data_keys.groupby("assignee")["task"].agg(list)
    data_by_assignee = pd.DataFrame({"Tasks": assignee_tasks_worked, "Estimated Hours": assignee_estimated_hours_worked, "Actual Hours Worked": assignee_actual_hours_worked, "Overcapacity": capacity_check})
    st.title("View by Employee")
    st.dataframe(data_by_assignee)
    


def view_three():
    project_for_view_three = dummy_data_keys["project"]
    tasks_for_view_three = dummy_data_keys["task"]
    task_ids_for_view_three = dummy_data_keys["task_id"]
    task_estimated_hours = dummy_data_keys["estimated_hours"]
    task_actual_hours = dummy_data_keys["actual_hours"]
    task_assignee = dummy_data_keys["assignee"]
    task_cost = task_actual_hours * dummy_data_keys["hourly_rate"]
    table_for_view_three = pd.DataFrame({"Project":project_for_view_three, "Tasks": tasks_for_view_three, "Task Id": task_ids_for_view_three, "Assignee":task_assignee, "Estimated Hours": task_estimated_hours, "Actual Hours":task_actual_hours, "Cost":task_cost  })
    st.title("View by Tasks")
    st.dataframe(table_for_view_three)
view_one()

#genre = st.radio(
    #"Which view would you like to see",
    #["View One: Team View", "View Two: View by Assignee", "View Three: Project/Task View"],
    #index=None,
#)

#st.write("You selected:", genre)

#if genre == "View One: Team View":
    #view_one() 

#if genre == "View Two: View by Assignee":
    #view_two() 

#if genre == "View Three: Project/Task View":
    #view_three() 
