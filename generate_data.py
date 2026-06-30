import csv
import random
from datetime import datetime, timedelta

def generate_mock_data(num_rows=500):
    random.seed(42)

    categories = ['Billing', 'Technical', 'General']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Open', 'Resolved', 'Escalated']
    agents = [f'AGT-{i:02d}' for i in range(1, 11)]

    base_time = datetime(2024, 1, 1)

    with open('support_tickets.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'ticket_id', 'created_at', 'category', 'priority', 'status', 
            'response_time_hrs', 'resolution_time_hrs', 'agent_id', 
            'customer_rating', 'issue_summary'
        ])

        for i in range(1, num_rows + 1):
            ticket_id = f'TKT-{i:03d}'
            created_at = base_time + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            category = random.choice(categories)
            
            if category == 'Technical':
                priority = random.choices(priorities, weights=[0.1, 0.3, 0.4, 0.2])[0]
            else:
                priority = random.choice(priorities)
                
            status = random.choices(statuses, weights=[0.2, 0.7, 0.1])[0]
            agent_id = random.choice(agents)
            
            if priority == 'Critical':
                resp_time_hrs = round(random.uniform(0.1, 2.0), 1)
            else:
                resp_time_hrs = round(random.uniform(0.5, 12.0), 1)
                
            if status == 'Resolved':
                resol_time_hrs = resp_time_hrs + round(random.uniform(0.5, 48.0), 1)
                if random.random() < 0.05:
                    resol_time_hrs += round(random.uniform(50.0, 150.0), 1)
                cust_rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.15, 0.3, 0.4])[0]
                if resol_time_hrs > 48:
                    cust_rating = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
            else:
                resol_time_hrs = ''
                cust_rating = ''
                
            issue_summary = f"{category} issue reported by user"
            if priority == 'Critical':
                issue_summary = f"CRITICAL: {category} system failure"

            writer.writerow([
                ticket_id,
                created_at.strftime('%Y-%m-%d %H:%M'),
                category,
                priority,
                status,
                resp_time_hrs,
                resol_time_hrs,
                agent_id,
                cust_rating,
                issue_summary
            ])
            
    print(f"Generated support_tickets.csv")

if __name__ == '__main__':
    generate_mock_data()
