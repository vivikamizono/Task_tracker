import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

TASKS_FILE = 'tasks.json'

def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
            # Add date to existing tasks if missing
            for task in tasks:
                if 'date' not in task:
                    task['date'] = datetime.now().strftime('%Y-%m-%d')
            return tasks
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

tasks = load_tasks()

@app.route('/')
def index():
    # Group tasks by date
    tasks_by_date = defaultdict(list)
    for task in tasks:
        tasks_by_date[task['date']].append(task)
    
    # Calculate total time for each day
    daily_totals = {}
    for date, day_tasks in tasks_by_date.items():
        daily_total = sum([timedelta(hours=task['hours'], minutes=task['minutes']) for task in day_tasks], timedelta())
        daily_totals[date] = str(daily_total)
    
    # Calculate overall total time
    total_time = sum([timedelta(hours=task['hours'], minutes=task['minutes']) for task in tasks], timedelta())
    
    return render_template('index.html', tasks_by_date=dict(tasks_by_date), daily_totals=daily_totals, total_time=total_time)

@app.route('/add_task', methods=['POST'])
def add_task():
    project_name = request.form['project_name']
    task_name = request.form['task_name']
    hours = int(request.form['hours'])
    minutes = int(request.form['minutes'])
    description = request.form['description']
    date = datetime.now().strftime('%Y-%m-%d')  # Get current date
    
    task = {
        'project_name': project_name,
        'name': task_name,
        'hours': hours,
        'minutes': minutes,
        'description': description,
        'date': date
    }
    
    tasks.append(task)
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)