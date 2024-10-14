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
            for i, task in enumerate(tasks):
                if 'date' not in task:
                    task['date'] = datetime.now().strftime('%Y-%m-%d')
                if 'id' not in task:
                    task['id'] = str(i)  # Ensure unique IDs
            return tasks
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def format_daily_summary(date, tasks):
    summary = f"Resumo do dia {date}:\n\n"
    total_time = timedelta()
    for task in tasks:
        time_spent = timedelta(hours=task['hours'])
        total_time += time_spent
        summary += f"- {task['project_name']}: {task['name']} ({task['hours']})  {task['description']}"
    summary += f"\nTempo total: {total_time}"
    return summary

tasks = load_tasks()

@app.route('/')
def index():
    tasks_by_date = defaultdict(list)
    for task in tasks:
        tasks_by_date[task['date']].append(task)
    
    daily_totals = {}
    daily_summaries = {}
    for date, day_tasks in tasks_by_date.items():
        daily_total = sum([timedelta(hours=task['hours']) for task in day_tasks], timedelta())
        daily_totals[date] = str(daily_total)
        daily_summaries[date] = format_daily_summary(date, day_tasks)
    
    total_time = sum([timedelta(hours=task['hours']) for task in tasks], timedelta())
    
    return render_template('index.html', tasks_by_date=dict(tasks_by_date), daily_totals=daily_totals, 
                           total_time=total_time, daily_summaries=daily_summaries)

@app.route('/add_task', methods=['POST'])
def add_task():
    project_name = request.form['project_name']
    task_name = request.form['task_name']
    hours = float(request.form['hours'])
    description = request.form['description']
    date = datetime.now().strftime('%d-%m-%Y')
    
    task = {
        'id': str(len(tasks)),  # Simple ID generation
        'project_name': project_name,
        'name': task_name,
        'hours': hours,
        'description': description,
        'date': date
    }
    
    tasks.append(task)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)