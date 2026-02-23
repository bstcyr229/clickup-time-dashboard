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
variance = dummy_data_keys["variance"]
team = dummy_data_keys["team"].unique()

def view_one():
    team_members = dummy_data_keys.groupby("team")["assignee"].nunique()
    team_hours_worked = dummy_data_keys.groupby("team")["actual_hours"].sum()
    

print(view_one())
