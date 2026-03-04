#Which of your teams is over or under capacity right now
#A deep dive on each of the members of your team, who is under capacity and who isn't
#An analysis of individual tasks, time spent vs time estimated 
#ClickUp API documentation link https://developer.clickup.com/reference/gettimeentrieswithinadaterange

import dummy_data as gdd
import pandas as pd
import streamlit as st


from dummy_data import generate_dummy_data

dummy_data_keys = gdd.generate_dummy_data()
#days_seperated = dummy_data_keys.groupby(["Team", "day"])["actual_hours"].sum().unstack()


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
        st.metric(label="Team One Total Capacity", value=f"{total_hours['Team One']}")
    with col2:
        st.metric(label="Team Two Total Capacity", value=f"{total_hours['Team Two']}")
    with col3:
        st.metric(label="Team Three Total Capacity", value=f"{total_hours['Team Three']}")
    with col4:
        st.metric(label="Team One Actual Hours Worked", value=f"{team_actual_hours_worked['Team One']}", delta=f"{over_capacity_percentage['Team One']:+.2f}%")
    with col5:
        st.metric(label="Team Two Actual Hours Worked", value=f"{team_actual_hours_worked['Team Two']}", delta=f"{over_capacity_percentage['Team Two']:+.2f}%")
    with col6:
        st.metric(label="Team Three Actual Hours Worked", value=f"{team_actual_hours_worked['Team Three']}", delta=f"{over_capacity_percentage['Team Three']:+.2f}%")
    with col7:
        st.metric(label="Team One Billable to Actual Hours Ratio", value=f"{(team_billable_hours['Team One'] / team_actual_hours_worked['Team One']):.2f}")
    with col8:
        st.metric(label="Team Two Billable to Actual Hours Ratio", value=f"{(team_billable_hours['Team Two'] / team_actual_hours_worked['Team Two']):.2f}")
    with col9:
        st.metric(label="Team Three Billable to Actual Hours Ratio", value=f"{team_billable_hours['Team Three']/ team_actual_hours_worked['Team Three']:.2f}")
    
    
    
    hours_by_team = pd.DataFrame({"Team Members":team_register_hours, "Team Capacity": total_hours , "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable":team_billable_hours , "Overcapacity":over_capacity, "Over Capacity Percentage" : over_capacity_percentage})
    hours_worked_by_team_and_day = pd.DataFrame({"Team One": team_register_hours, "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Billable Hours Worked": team_billable_hours, "Overcapacity":over_capacity})
    st.title("Team View")
    st.dataframe(data=hours_by_team)
    st.dataframe(data= hours_worked_by_team_and_day)
    
    days_seperated_for_graph = dummy_data_keys.groupby(["Team", "day"])["actual_hours"].sum().unstack().transpose().reset_index()
    st.write("Actual Hours Worked by Team and Day")
    st.area_chart(data=days_seperated_for_graph, x="day", y=["Team One", "Team Two", "Team Three"], use_container_width=True) 


def view_two():
    assignee_estimated_hours_worked = dummy_data_keys.groupby("assignee")["estimated_hours"].sum()
    assignee_actual_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    assignee_total_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    capacity_check = assignee_total_hours_worked > 40
    assignee_tasks_worked = dummy_data_keys.groupby("assignee")["task"].agg(list)
    data_by_assignee = pd.DataFrame({"Tasks": assignee_tasks_worked, "Estimated Hours": assignee_estimated_hours_worked, "Actual Hours Worked": assignee_actual_hours_worked, "Billable Hours Worked":dummy_data_keys.groupby("assignee")['billable_hours'].sum(), "Overcapacity": capacity_check})
    st.title("View by Employee")
    st.dataframe(data_by_assignee)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        st.metric(label="Assignee Average Estimated Hours Worked", value=f"{assignee_estimated_hours_worked.mean():.2f}")
    with col2:
        st.metric(label="Assignee Average Actual Hours Worked", value=f"{assignee_actual_hours_worked.mean():.2f}")
    with col3:
        st.metric(label="Assignee Average Billable Hours Worked", value=f"{(dummy_data_keys.groupby('assignee')['billable_hours'].sum()).mean():.2f}")

    new_x_index = data_by_assignee.reset_index()
    st.write("Estimated Hours vs Actual Hours Worked by Assignee")
    st.area_chart(data=new_x_index, x='assignee', y=["Estimated Hours", "Actual Hours Worked"], use_container_width=True)



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

genre = st.radio(
    "Which view would you like to see",
    ["View One: Team View", "View Two: View by Assignee", "View Three: Project/Task View"],
    index=None,
)

st.write("You selected:", genre)

if genre == "View One: Team View":
    view_one() 

if genre == "View Two: View by Assignee":
    view_two() 

if genre == "View Three: Project/Task View":
    view_three() 
