#Which of your teams is over or under capacity right now
#A deep dive on each of the members of your team, who is under capacity and who isn't
#An analysis of individual tasks, time spent vs time estimated 

import dummy_data as gdd
import pandas as pd


from dummy_data import generate_dummy_data

dummy_data_keys = gdd.generate_dummy_data()
assignee = dummy_data_keys["assignee"].unique().tolist()
project = dummy_data_keys["project"].unique().tolist()
actual_hours = dummy_data_keys["actual_hours"]
estimated_hours = dummy_data_keys["estimated_hours"]
variance = dummy_data_keys["variance"]
team = dummy_data_keys["Team"].unique()
team_register = dummy_data_keys["Team"]
team_register_two = dummy_data_keys.groupby("Team")["assignee"].unique()
tasks = dummy_data_keys["task"]



def view_one():
    team_members = dummy_data_keys.groupby("Team")["assignee"].unique()
    team_members_number = team_members.apply(len)
    team_estimated_hours_worked = dummy_data_keys.groupby("Team")["estimated_hours"].sum()
    team_actual_hours_worked = dummy_data_keys.groupby("Team")["actual_hours"].sum()
    difference_in_hours = team_actual_hours_worked - team_estimated_hours_worked
    total_hours = team_members_number * 40
    over_capacity = total_hours < team_actual_hours_worked
    over_capacity_percentage = round(((team_actual_hours_worked / total_hours ) * 100) - 100 )
    hours_by_team = pd.DataFrame({"Team Members":team_register_two, "Team Capacity": total_hours , "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Difference": difference_in_hours, "Overcapacity":over_capacity, "Over Capacity Percentage" : over_capacity_percentage})
    print(hours_by_team)

def view_two():
    assignee_estimated_hours_worked = dummy_data_keys.groupby("assignee")["estimated_hours"].sum()
    assignee_actual_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    assginee_total_hours_worked = dummy_data_keys.groupby("assignee")["actual_hours"].sum()
    capacity_check = assginee_total_hours_worked > 40
    assignee_tasks_worked = dummy_data_keys.groupby("assignee")["task"].agg(list)
    data_by_assignee = pd.DataFrame({"Tasks": assignee_tasks_worked, "Estimated Hours": assignee_estimated_hours_worked, "Actual Hours Worked": assignee_actual_hours_worked, "Overcapacity": capacity_check})
    print(data_by_assignee)
