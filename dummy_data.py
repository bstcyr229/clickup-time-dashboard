import pandas as pd
import random

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
    rows = []


    for _ in range(60):
        estimated = round(random.uniform(1,12),1)
        actual = round(estimated * random.uniform(0.5, 2.0),1)
        selected_assignee = random.choice(staff)
        team_register = teams[selected_assignee]

        rows.append({
            "assignee": selected_assignee,
            "project":random.choice(projects),
            "task":random.choice(tasks),
            "estimated_hours":estimated,
            "actual_hours":actual,
            "variance": round(actual - estimated,1),
            "Team": team_register, 
            

        })

    
    return pd.DataFrame(rows)
    
if __name__ == "__main__":
    df= generate_dummy_data()
    print(df.head(10))
    print(f"\n{len(df)} tasks generated")