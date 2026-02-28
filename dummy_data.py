import pandas as pd
import random
import uuid 

def generate_dummy_data():
    staff = ["Joe", "Sofia", "Marcus", "Leila" , "Khalid" , "Eva" , "Pierre"]
    projects = ["Website Redesign", "CRM Migration", "Onboarding Revamp", "Q2 Reporting"]
    tasks = [
        "Kickoff call", "Scope doc", "Design review", "Dev sprint",
        "QA testing", "Stakeholder update", "Final delivery", "Retrospective"
    ]
    teams = {
        "Joe" : "Team One", "Sofia" : "Team Two" , "Marcus" : "Team Three", "Leila": "Team One" , "Khalid" : "Team Two" , "Eva" : "Team Three", "Pierre"
    : "Team One"}

    rates = {
    "Joe": 85,
    "Sofia": 95,
    "Marcus": 90,
    "Leila": 80,
    "Khalid": 100,
    "Eva": 110,
    "Pierre": 75
}
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    work_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    rows = []
    
    estimated = round(random.uniform(1,12),1)
    actual = round(estimated * random.uniform(0.5, 2.0),1)
    #estimated = int(estimated)
    #actual = int(actual) 


    for _ in range(60):
        estimated = round(random.uniform(1,12),1)
        actual = round(estimated * random.uniform(0.5, 2.0),1)
        selected_assignee = random.choice(staff)
        team_register = teams[selected_assignee]
        task_id = uuid.uuid4()
        task_id = str(task_id)

        rows.append({
            "assignee": selected_assignee,
            "project":random.choice(projects),
            "task":random.choice(tasks),
            "task_id": task_id[0:5],
            "estimated_hours":estimated,
            "actual_hours":actual,
            "variance": round(actual - estimated,1),
            "Team": team_register, 
            "hourly_rate": rates[selected_assignee],
            "total_cost": round(actual * rates[selected_assignee],2),
            "day": random.choice(work_days),

            

        })

    
    return pd.DataFrame(rows)
    
if __name__ == "__main__":
    df= generate_dummy_data()
    print(df.head(10))
    print(f"\n{len(df)} tasks generated")