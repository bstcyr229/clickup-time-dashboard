#View One, show hours by team: Key: Team {Name here} Values: Assignees, total hours worked
    #Gather the assignees and hours worked key pairs 
    #Reduce to unique values for asignees 
    #Sum the hours for each assignee
    #Print the view  
#View Two, shows hours worked by assignee vs hours estimated : Key Assignee: total hours worked, total hours estimated
#View Three, shows a task and all data points for it and only it, Key: Task Values: Assignee project actual hours and variance

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



def view_one():
    team_members = dummy_data_keys.groupby("Team")["assignee"].nunique()
    team_estimated_hours_worked = dummy_data_keys.groupby("Team")["estimated_hours"].sum()
    team_actual_hours_worked = dummy_data_keys.groupby("Team")["actual_hours"].sum()
    difference_in_hours = team_actual_hours_worked - team_estimated_hours_worked
    total_hours = team_members * 40
    over_capacity = total_hours < team_actual_hours_worked
    over_capacity_percentage = round(((team_actual_hours_worked / total_hours ) * 100) - 100 )
    hours_by_team = pd.DataFrame({"Team Members":team_register_two, "Team Capacity": total_hours , "Estimated Hours Worked": team_estimated_hours_worked, "Actual Hours Worked": team_actual_hours_worked, "Difference": difference_in_hours, "Overcapacity":over_capacity, "Over Capacity Percentage" : over_capacity_percentage})
    print(hours_by_team)
    

print(view_one())
