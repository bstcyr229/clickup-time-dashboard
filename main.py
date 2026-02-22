#View One, show hours by team: Key: Team {Name here} Values: Assignees, total hours worked
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

master_data_dictionary = {
    "Assignee": assignee,  
    "Project": project,
    "Actual Hours":actual_hours,
    "Variance": variance
}

def view_one():
    pass
    