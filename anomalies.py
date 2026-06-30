import pandas as pd
import sqlite3
from datetime import datetime
import json

DB_PATH = "tickets.db"

def get_anomalies():
    """
    Detect anomalies in the support tickets dataset.
    Returns a dictionary with rule-based and statistical anomalies.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM tickets", conn)
        conn.close()
    except Exception as e:
        return {"error": str(e)}

    anomalies = {
        "rule_based": [],
        "statistical": []
    }

    if df.empty:
        return anomalies

    # Convert created_at to datetime objects
    df['created_at_dt'] = pd.to_datetime(df['created_at'])
    now = df['created_at_dt'].max() if not df.empty else datetime.now()

    # Rule 1: Unresolved High/Critical priority tickets older than 24 hours
    unresolved_mask = df['status'].isin(['Open', 'Escalated'])
    high_priority_mask = df['priority'].isin(['High', 'Critical'])
    
    # Calculate age in hours
    df['age_hours'] = (now - df['created_at_dt']).dt.total_seconds() / 3600
    
    rule1_anomalies = df[unresolved_mask & high_priority_mask & (df['age_hours'] > 24)]
    
    for _, row in rule1_anomalies.iterrows():
        anomalies["rule_based"].append({
            "ticket_id": row['ticket_id'],
            "reason": f"Unresolved {row['priority']} ticket older than 24 hours ({row['age_hours']:.1f} hrs old)",
            "agent_id": row['agent_id']
        })

    # Statistical Anomaly: Abnormally long resolution times (Z-score > 2.5) per category
    resolved_df = df[df['resolution_time_hrs'].notna()].copy()
    if not resolved_df.empty:
        for category in resolved_df['category'].unique():
            cat_df = resolved_df[resolved_df['category'] == category]
            if len(cat_df) > 3:  # Need enough data points for stats
                mean_res = cat_df['resolution_time_hrs'].mean()
                std_res = cat_df['resolution_time_hrs'].std()
                
                if std_res > 0:
                    cat_df['z_score'] = (cat_df['resolution_time_hrs'] - mean_res) / std_res
                    outliers = cat_df[cat_df['z_score'] > 2.5]
                    
                    for _, row in outliers.iterrows():
                        anomalies["statistical"].append({
                            "ticket_id": row['ticket_id'],
                            "reason": f"Abnormally long resolution time for {category} category ({row['resolution_time_hrs']} hrs, avg is {mean_res:.1f} hrs)",
                            "agent_id": row['agent_id']
                        })

    return anomalies

if __name__ == "__main__":
    print(json.dumps(get_anomalies(), indent=2))
