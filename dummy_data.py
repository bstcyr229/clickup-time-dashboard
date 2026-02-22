import pandas as pd
import random

def generate_dummy_data():
    team = ["Joe", "Sofia", "Marcus", "Leila"]
    projects = ["Website Redesign", "CRM Migration", "Onboarding Revamp", "Q2 Reporting"]
    tasks = [
        "Kickoff call", "Scope doc", "Design review", "Dev sprint",
        "QA testing", "Stakeholder update", "Final delivery", "Retrospective"
    ]

    rows = []

    for _ in range(60):
        estimated = round(random.uniform(1,12),1)
        actual = round(estimated * random.uniform(0.5, 2.0),1)
        rows.append({
            "assignee": random.choice(team),
            "project":random.choice(projects),
            "task":random.choice(tasks),
            "estimated_hours":estimated,
            "actual_hours":actual,
            "variance": round(actual - estimated,1)

        })

    return pd.DataFrame(rows)
    
if __name__ == "__main__":
    df= generate_dummy_data()
    print(df.head(10))
    print(f"\n{len(df)} tasks generated")